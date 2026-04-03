from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
import time
from apps.core.models import Project, File, CodeGeneration, ExecutionResult, Session
from .serializers import (
    ProjectSerializer, FileSerializer, CodeGenerationSerializer,
    ExecutionResultSerializer, SessionSerializer, ProjectListSerializer
)
from .services import OllamaService, CodeExecutionService
import logging

logger = logging.getLogger(__name__)


class BaseViewSet(viewsets.GenericViewSet):
    """Base ViewSet with common functionality"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def handle_exception(self, exc):
        logger.error(f"API error: {str(exc)}", exc_info=True)
        return super().handle_exception(exc)


class ProjectViewSet(BaseViewSet,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Project.objects.prefetch_related(
        Prefetch('files', queryset=File.objects.order_by('path'))
    ).all()
    serializer_class = ProjectSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer
    
    @action(detail=True, methods=['get'], url_path='files')
    def list_files(self, request, pk=None):
        """Get all files for a project"""
        project = self.get_object()
        files = project.files.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='files')
    def create_file(self, request, pk=None):
        """Create a new file in the project"""
        project = self.get_object()
        
        name = request.data.get('name', 'untitled')
        path = request.data.get('path', f'untitled_{int(time.time())}.txt')
        language = request.data.get('language', 'text')
        content = request.data.get('content', '')
        
        # Validate required fields
        if not name or not path:
            return Response(
                {'error': 'name and path are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            file = File.objects.create(
                project=project,
                name=name,
                path=path,
                language=language,
                content=content
            )
            serializer = FileSerializer(file)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating file: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class FileViewSet(BaseViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    queryset = File.objects.select_related('project').all()
    serializer_class = FileSerializer
    
    def get_queryset(self):
        """Filter files by project if provided"""
        queryset = super().get_queryset()
        project_id = self.request.query_params.get('project_id')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset
    
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        """Execute the file content"""
        file = self.get_object()
        service = CodeExecutionService()
        
        try:
            result = service.execute(file.content, file.language)
            
            execution = ExecutionResult.objects.create(
                file=file,
                language=file.language,
                stdout=result.get('stdout', ''),
                stderr=result.get('stderr', ''),
                exit_code=result.get('exit_code', 0),
                execution_time=result.get('execution_time', 0)
            )
            
            serializer = ExecutionResultSerializer(execution)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Execution error: {str(e)}", exc_info=True)
            return Response(
                {'error': f'Execution failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='by-project')
    def by_project(self, request):
        """Get files filtered by project ID"""
        project_id = request.query_params.get('project_id')
        
        if not project_id:
            return Response(
                {'error': 'project_id query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        files = File.objects.filter(project_id=project_id).order_by('path')
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)


class CodeGenerationViewSet(BaseViewSet,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin):
    queryset = CodeGeneration.objects.select_related('project').all()
    serializer_class = CodeGenerationSerializer
    
    def get_queryset(self):
        """Filter generations by project if provided"""
        queryset = super().get_queryset()
        project_id = self.request.query_params.get('project_id')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate code using AI"""
        project_id = request.data.get('project_id')
        prompt = request.data.get('prompt')
        language = request.data.get('language', 'python')
        
        # Validate required fields
        if not project_id or not prompt:
            return Response(
                {'error': 'project_id and prompt are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        project = get_object_or_404(Project, id=project_id)
        service = OllamaService()
        
        try:
            generated_code = service.generate_code(prompt, language)
            
            generation = CodeGeneration.objects.create(
                project=project,
                prompt=prompt,
                generated_code=generated_code,
                language=language,
                model_used='codellama'
            )
            
            serializer = CodeGenerationSerializer(generation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Generation error: {str(e)}", exc_info=True)
            return Response(
                {'error': f'Code generation failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='by-project')
    def by_project(self, request):
        """Get generations filtered by project ID"""
        project_id = request.query_params.get('project_id')
        
        if not project_id:
            return Response(
                {'error': 'project_id query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        generations = CodeGeneration.objects.filter(
            project_id=project_id
        ).order_by('-created_at')
        
        serializer = CodeGenerationSerializer(generations, many=True)
        return Response(serializer.data)


class SessionViewSet(BaseViewSet,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Session.objects.select_related('project', 'active_file').all()
    serializer_class = SessionSerializer
    
    @action(detail=True, methods=['patch'], url_path='cursor')
    def update_cursor(self, request, pk=None):
        """Update cursor position for a session"""
        session = self.get_object()
        cursor_position = request.data.get('cursor_position')
        
        if cursor_position is None:
            return Response(
                {'error': 'cursor_position is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session.cursor_position = cursor_position
        session.save(update_fields=['cursor_position', 'updated_at'])
        
        serializer = SessionSerializer(session)
        return Response(serializer.data)
