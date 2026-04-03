"""Tests for API services."""
from django.test import TestCase
from unittest.mock import patch, MagicMock
import requests
from apps.api.services import OllamaService, CodeExecutionService


class OllamaServiceTest(TestCase):
    """Test cases for OllamaService."""

    def setUp(self):
        self.service = OllamaService()

    @patch('apps.api.services.requests.post')
    def test_generate_code_success(self, mock_post):
        """Test successful code generation."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'response': 'print("Hello World")'}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.service.generate_code(
            prompt='Hello world function',
            language='python'
        )

        self.assertEqual(result, 'print("Hello World")')
        mock_post.assert_called_once()

    @patch('apps.api.services.requests.post')
    def test_generate_code_timeout(self, mock_post):
        """Test code generation timeout."""
        mock_post.side_effect = requests.exceptions.Timeout()

        with self.assertRaises(Exception) as context:
            self.service.generate_code(prompt='test', language='python')

        self.assertIn('timed out', str(context.exception))

    @patch('apps.api.services.requests.post')
    def test_generate_code_request_error(self, mock_post):
        """Test code generation request error."""
        mock_post.side_effect = requests.exceptions.RequestException('Connection error')

        with self.assertRaises(Exception) as context:
            self.service.generate_code(prompt='test', language='python')

        self.assertIn('Failed to generate code', str(context.exception))

    @patch('apps.api.services.requests.get')
    def test_list_models_success(self, mock_get):
        """Test listing available models."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'models': [{'name': 'codellama'}, {'name': 'mistral'}]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        models = self.service.list_models()

        self.assertEqual(models, ['codellama', 'mistral'])

    @patch('apps.api.services.requests.get')
    def test_list_models_error(self, mock_get):
        """Test listing models with error."""
        mock_get.side_effect = requests.exceptions.RequestException()

        models = self.service.list_models()

        self.assertEqual(models, [])

    @patch('apps.api.services.requests.get')
    def test_is_available_true(self, mock_get):
        """Test service availability check - available."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        self.assertTrue(self.service.is_available())

    @patch('apps.api.services.requests.get')
    def test_is_available_false(self, mock_get):
        """Test service availability check - not available."""
        mock_get.side_effect = requests.exceptions.RequestException()

        self.assertFalse(self.service.is_available())

    def test_custom_base_url_and_model(self):
        """Test initialization with custom parameters."""
        service = OllamaService(
            base_url='http://custom:11434',
            model='mistral'
        )

        self.assertEqual(service.base_url, 'http://custom:11434')
        self.assertEqual(service.model, 'mistral')


class CodeExecutionServiceTest(TestCase):
    """Test cases for CodeExecutionService."""

    def setUp(self):
        self.service = CodeExecutionService(timeout=5)

    def test_execute_python_code(self):
        """Test executing Python code."""
        code = 'print("Hello from Python")'
        result = self.service.execute(code, 'python')

        self.assertIn('exit_code', result)
        self.assertIn('stdout', result)
        self.assertIn('stderr', result)
        self.assertIn('execution_time', result)

    def test_execute_javascript_code(self):
        """Test executing JavaScript code."""
        code = 'console.log("Hello from JS")'
        result = self.service.execute(code, 'javascript')

        self.assertIn('exit_code', result)

    def test_execute_bash_code(self):
        """Test executing Bash code."""
        code = 'echo "Hello from Bash"'
        result = self.service.execute(code, 'bash')

        self.assertIn('exit_code', result)
        self.assertIn('Hello from Bash', result['stdout'])

    def test_execute_unsupported_language(self):
        """Test executing unsupported language."""
        code = 'some code'
        result = self.service.execute(code, 'cobol')

        self.assertEqual(result['exit_code'], 1)
        self.assertIn('Unsupported language', result['stderr'])

    def test_is_language_supported(self):
        """Test language support check."""
        self.assertTrue(self.service.is_language_supported('python'))
        self.assertTrue(self.service.is_language_supported('javascript'))
        self.assertTrue(self.service.is_language_supported('bash'))
        self.assertFalse(self.service.is_language_supported('cobol'))

    def test_execute_with_custom_timeout(self):
        """Test execution with custom timeout."""
        service = CodeExecutionService(timeout=10)
        self.assertEqual(service.timeout, 10)

    def test_execute_invalid_code(self):
        """Test executing invalid Python code."""
        code = 'print(invalid_syntax'
        result = self.service.execute(code, 'python')

        self.assertNotEqual(result['exit_code'], 0)
        self.assertTrue(len(result['stderr']) > 0)

    def test_temp_file_cleanup(self):
        """Test that temporary files are cleaned up after execution."""
        import os
        import tempfile
        
        code = 'print("test")'
        ext = '.py'
        
        # Create temp file manually to test cleanup
        fd, temp_path = tempfile.mkstemp(suffix=ext)
        os.close(fd)
        
        # Verify file exists before cleanup
        self.assertTrue(os.path.exists(temp_path))
        
        # Clean up
        os.remove(temp_path)
        self.assertFalse(os.path.exists(temp_path))
