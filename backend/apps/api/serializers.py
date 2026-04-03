from rest_framework import serializers
from apps.core.models import Project, File, CodeGeneration, ExecutionResult, Session


class FileSerializer(serializers.ModelSerializer):
    """Serializer for File model"""
    
    class Meta:
        model = File
        fields = ['id', 'name', 'path', 'content', 'language', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ProjectListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for project list view"""
    file_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'file_count', 'created_at', 'updated_at']
    
    def get_file_count(self, obj):
        return obj.files.count() if hasattr(obj, 'files') else 0


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model with nested files"""
    files = FileSerializer(many=True, read_only=True)
    file_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'files', 'file_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_file_count(self, obj):
        return obj.files.count() if hasattr(obj, 'files') else 0


class CodeGenerationSerializer(serializers.ModelSerializer):
    """Serializer for CodeGeneration model"""
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = CodeGeneration
        fields = [
            'id', 'project', 'project_name', 'prompt', 'generated_code',
            'language', 'model_used', 'created_at'
        ]
        read_only_fields = ['created_at', 'model_used']


class ExecutionResultSerializer(serializers.ModelSerializer):
    """Serializer for ExecutionResult model"""
    file_name = serializers.CharField(source='file.name', read_only=True)
    
    class Meta:
        model = ExecutionResult
        fields = [
            'id', 'file', 'file_name', 'language', 'stdout', 'stderr',
            'exit_code', 'execution_time', 'created_at'
        ]
        read_only_fields = ['created_at']


class SessionSerializer(serializers.ModelSerializer):
    """Serializer for Session model"""
    project_name = serializers.CharField(source='project.name', read_only=True)
    active_file_name = serializers.CharField(source='active_file.name', read_only=True)
    
    class Meta:
        model = Session
        fields = [
            'id', 'project', 'project_name', 'name', 'active_file',
            'active_file_name', 'cursor_position', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
