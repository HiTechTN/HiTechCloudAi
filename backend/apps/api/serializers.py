from rest_framework import serializers
from apps.core.models import Project, File, CodeGeneration, ExecutionResult, Session

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'path', 'content', 'language', 'created_at', 'updated_at']

class ProjectSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)
    file_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'files', 'file_count', 'created_at', 'updated_at']

    def get_file_count(self, obj):
        return obj.files.count()

class CodeGenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeGeneration
        fields = ['id', 'project', 'prompt', 'generated_code', 'language', 'model_used', 'created_at']

class ExecutionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutionResult
        fields = ['id', 'file', 'language', 'stdout', 'stderr', 'exit_code', 'execution_time', 'created_at']

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'project', 'name', 'active_file', 'cursor_position', 'created_at', 'updated_at']
