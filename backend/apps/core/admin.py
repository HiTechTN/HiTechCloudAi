from django.contrib import admin
from .models import Project, File, CodeGeneration, ExecutionResult, Session

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'language', 'created_at')
    search_fields = ('name', 'path')
    list_filter = ('language', 'project')

@admin.register(CodeGeneration)
class CodeGenerationAdmin(admin.ModelAdmin):
    list_display = ('project', 'language', 'model_used', 'created_at')
    list_filter = ('language', 'model_used')

@admin.register(ExecutionResult)
class ExecutionResultAdmin(admin.ModelAdmin):
    list_display = ('file', 'language', 'exit_code', 'created_at')
    list_filter = ('language', 'exit_code')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'created_at', 'updated_at')
    list_filter = ('project',)
