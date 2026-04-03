"""Tests for core models."""
from django.test import TestCase
from django.utils import timezone
from apps.core.models import Project, File, CodeGeneration, ExecutionResult, Session


class ProjectModelTest(TestCase):
    """Test cases for Project model."""

    def test_create_project(self):
        """Test creating a project."""
        project = Project.objects.create(
            name='Test Project',
            description='A test project'
        )
        
        self.assertEqual(str(project), 'Test Project')
        self.assertIsNotNone(project.created_at)
        self.assertIsNotNone(project.updated_at)

    def test_project_ordering(self):
        """Test that projects are ordered by updated_at descending."""
        project1 = Project.objects.create(name='Project 1')
        project2 = Project.objects.create(name='Project 2')
        
        # Update project1 to make it more recent
        project1.name = 'Updated Project 1'
        project1.save()
        
        projects = list(Project.objects.all())
        self.assertEqual(projects[0].name, 'Updated Project 1')


class FileModelTest(TestCase):
    """Test cases for File model."""

    def setUp(self):
        self.project = Project.objects.create(name='Test Project')

    def test_create_file(self):
        """Test creating a file."""
        file = File.objects.create(
            project=self.project,
            name='test.py',
            path='test.py',
            content='print("hello")',
            language='python'
        )
        
        self.assertEqual(str(file), 'Test Project/test.py')
        self.assertEqual(file.content, 'print("hello")')
        self.assertEqual(file.language, 'python')

    def test_file_unique_constraint(self):
        """Test unique constraint on project and path."""
        File.objects.create(
            project=self.project,
            name='test.py',
            path='test.py',
            content='content1'
        )
        
        with self.assertRaises(Exception):
            File.objects.create(
                project=self.project,
                name='test2.py',
                path='test.py',
                content='content2'
            )

    def test_file_ordering(self):
        """Test that files are ordered by path."""
        File.objects.create(
            project=self.project,
            name='z_file.py',
            path='z_file.py',
            content=''
        )
        File.objects.create(
            project=self.project,
            name='a_file.py',
            path='a_file.py',
            content=''
        )
        
        files = list(File.objects.all())
        self.assertEqual(files[0].path, 'a_file.py')
        self.assertEqual(files[1].path, 'z_file.py')


class CodeGenerationModelTest(TestCase):
    """Test cases for CodeGeneration model."""

    def setUp(self):
        self.project = Project.objects.create(name='Test Project')

    def test_create_generation(self):
        """Test creating a code generation."""
        generation = CodeGeneration.objects.create(
            project=self.project,
            prompt='Create a hello world function',
            generated_code='print("Hello World")',
            language='python',
            model_used='codellama'
        )
        
        self.assertIn('Test Project', str(generation))
        self.assertEqual(generation.generated_code, 'print("Hello World")')
        self.assertEqual(generation.model_used, 'codellama')

    def test_generation_ordering(self):
        """Test that generations are ordered by created_at descending."""
        gen1 = CodeGeneration.objects.create(
            project=self.project,
            prompt='First',
            generated_code='code1'
        )
        gen2 = CodeGeneration.objects.create(
            project=self.project,
            prompt='Second',
            generated_code='code2'
        )
        
        generations = list(CodeGeneration.objects.all())
        self.assertEqual(generations[0].prompt, 'Second')


class ExecutionResultModelTest(TestCase):
    """Test cases for ExecutionResult model."""

    def setUp(self):
        self.project = Project.objects.create(name='Test Project')
        self.file = File.objects.create(
            project=self.project,
            name='test.py',
            path='test.py',
            content='print("hello")',
            language='python'
        )

    def test_create_execution_result(self):
        """Test creating an execution result."""
        result = ExecutionResult.objects.create(
            file=self.file,
            language='python',
            stdout='hello\n',
            stderr='',
            exit_code=0,
            execution_time=0.5
        )
        
        self.assertEqual(str(result), 'Execution of test.py')
        self.assertEqual(result.stdout, 'hello\n')
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.execution_time, 0.5)

    def test_execution_result_ordering(self):
        """Test that results are ordered by created_at descending."""
        result1 = ExecutionResult.objects.create(
            file=self.file,
            language='python',
            stdout='result1',
            exit_code=0
        )
        result2 = ExecutionResult.objects.create(
            file=self.file,
            language='python',
            stdout='result2',
            exit_code=0
        )
        
        results = list(ExecutionResult.objects.all())
        self.assertEqual(results[0].stdout, 'result2')


class SessionModelTest(TestCase):
    """Test cases for Session model."""

    def setUp(self):
        self.project = Project.objects.create(name='Test Project')
        self.file = File.objects.create(
            project=self.project,
            name='test.py',
            path='test.py',
            content='print("hello")',
            language='python'
        )

    def test_create_session(self):
        """Test creating a session."""
        session = Session.objects.create(
            project=self.project,
            name='Test Session',
            active_file=self.file,
            cursor_position=42
        )
        
        self.assertEqual(str(session), 'Test Project - Test Session')
        self.assertEqual(session.cursor_position, 42)
        self.assertEqual(session.active_file, self.file)

    def test_session_with_null_active_file(self):
        """Test creating a session without an active file."""
        session = Session.objects.create(
            project=self.project,
            name='Empty Session',
            active_file=None,
            cursor_position=0
        )
        
        self.assertIsNone(session.active_file)
        self.assertEqual(session.cursor_position, 0)

    def test_session_ordering(self):
        """Test that sessions are ordered by updated_at descending."""
        session1 = Session.objects.create(
            project=self.project,
            name='Session 1'
        )
        session2 = Session.objects.create(
            project=self.project,
            name='Session 2'
        )
        
        # Update session1
        session1.cursor_position = 10
        session1.save()
        
        sessions = list(Session.objects.all())
        self.assertEqual(sessions[0].name, 'Session 1')
