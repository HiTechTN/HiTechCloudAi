from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.core.models import Project, File, CodeGeneration, ExecutionResult, Session
from .serializers import ProjectSerializer, FileSerializer, CodeGenerationSerializer, ExecutionResultSerializer, SessionSerializer
from .services import OllamaService, CodeExecutionService
import logging

logger = logging.getLogger(__name__)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True, methods=['get'])
    def files(self, request, pk=None):
        project = self.get_object()
        files = project.files.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def create_file(self, request, pk=None):
        project = self.get_object()
        file = File.objects.create(
            project=project,
            name=request.data.get('name', 'untitled'),
            path=request.data.get('path', 'untitled.txt'),
            language=request.data.get('language', 'text'),
            content=request.data.get('content', '')
        )
        serializer = FileSerializer(file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
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
            logger.error(f"Execution error: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def by_project(self, request):
        project_id = request.query_params.get('project_id')
        if not project_id:
            return Response({'error': 'project_id required'}, status=status.HTTP_400_BAD_REQUEST)
        files = File.objects.filter(project_id=project_id)
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)


class CodeGenerationViewSet(viewsets.ModelViewSet):
    queryset = CodeGeneration.objects.all()
    serializer_class = CodeGenerationSerializer

    @action(detail=False, methods=['post'])
    def generate(self, request):
        project_id = request.data.get('project_id')
        prompt = request.data.get('prompt')
        language = request.data.get('language', 'python')

        if not project_id or not prompt:
            return Response({'error': 'project_id and prompt required'}, status=status.HTTP_400_BAD_REQUEST)

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
            logger.error(f"Generation error: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def by_project(self, request):
        project_id = request.query_params.get('project_id')
        if not project_id:
            return Response({'error': 'project_id required'}, status=status.HTTP_400_BAD_REQUEST)
        generations = CodeGeneration.objects.filter(project_id=project_id)
        serializer = CodeGenerationSerializer(generations, many=True)
        return Response(serializer.data)


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['patch'])
    def update_cursor(self, request, pk=None):
        session = self.get_object()
        session.cursor_position = request.data.get('cursor_position', 0)
        session.save()
        serializer = SessionSerializer(session)
        return Response(serializer.data)
