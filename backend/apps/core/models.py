from django.db import models
from django.utils import timezone

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name


class File(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=1024)
    content = models.TextField(blank=True, default='')
    language = models.CharField(max_length=50, default='text')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['path']
        unique_together = ('project', 'path')

    def __str__(self):
        return f"{self.project.name}/{self.path}"


class CodeGeneration(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='generations')
    prompt = models.TextField()
    generated_code = models.TextField()
    language = models.CharField(max_length=50, default='python')
    model_used = models.CharField(max_length=100, default='codellama')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Generation in {self.project.name} at {self.created_at}"


class ExecutionResult(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='executions')
    language = models.CharField(max_length=50)
    stdout = models.TextField(blank=True, default='')
    stderr = models.TextField(blank=True, default='')
    exit_code = models.IntegerField(default=0)
    execution_time = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Execution of {self.file.name}"


class Session(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sessions')
    name = models.CharField(max_length=255)
    active_file = models.ForeignKey(File, on_delete=models.SET_NULL, null=True, blank=True)
    cursor_position = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.project.name} - {self.name}"
