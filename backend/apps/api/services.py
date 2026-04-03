import os
import requests
import subprocess
import time
import tempfile
import logging
from typing import Dict, Any, Optional
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class OllamaService:
    """Service for interacting with Ollama API for code generation"""
    
    DEFAULT_MODEL = 'codellama'
    DEFAULT_TIMEOUT = 60
    DEFAULT_URL = 'http://localhost:11434'
    
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.base_url = base_url or os.getenv('OLLAMA_API_URL', self.DEFAULT_URL)
        self.model = model or self.DEFAULT_MODEL
    
    def generate_code(self, prompt: str, language: str = 'python') -> str:
        """Generate code using Ollama API
        
        Args:
            prompt: The code generation prompt
            language: Target programming language
            
        Returns:
            Generated code as string
            
        Raises:
            Exception: If code generation fails
        """
        try:
            formatted_prompt = f"Generate {language} code for: {prompt}"
            
            response = requests.post(
                f'{self.base_url}/api/generate',
                json={
                    'model': self.model,
                    'prompt': formatted_prompt,
                    'stream': False,
                },
                timeout=self.DEFAULT_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            return data.get('response', '')
            
        except requests.exceptions.Timeout:
            logger.error(f"Ollama API timeout after {self.DEFAULT_TIMEOUT}s")
            raise Exception("Code generation timed out")
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API error: {str(e)}")
            raise Exception(f"Failed to generate code with Ollama: {str(e)}")
    
    def list_models(self) -> list:
        """List available Ollama models
        
        Returns:
            List of model names
        """
        try:
            response = requests.get(f'{self.base_url}/api/tags', timeout=10)
            response.raise_for_status()
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API error: {str(e)}")
            return []
    
    def is_available(self) -> bool:
        """Check if Ollama service is available
        
        Returns:
            True if service is reachable, False otherwise
        """
        try:
            response = requests.get(f'{self.base_url}/api/tags', timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False


class CodeExecutionService:
    """Service for executing code in multiple languages"""
    
    LANGUAGE_EXTENSIONS = {
        'python': '.py',
        'javascript': '.js',
        'typescript': '.ts',
        'bash': '.sh',
        'go': '.go',
        'rust': '.rs',
        'java': '.java',
    }

    LANGUAGE_COMMANDS = {
        'python': 'python',
        'javascript': 'node',
        'typescript': 'ts-node',
        'bash': 'bash',
        'go': 'go run',
        'rust': 'rustc',
        'java': 'javac',
    }
    
    DEFAULT_TIMEOUT = 30
    
    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        self.timeout = timeout
    
    @contextmanager
    def _temp_file(self, code: str, extension: str):
        """Context manager for temporary file creation and cleanup
        
        Args:
            code: Code content to write
            extension: File extension
            
        Yields:
            Path to temporary file
        """
        temp_file = None
        try:
            fd, temp_file = tempfile.mkstemp(suffix=extension)
            with os.fdopen(fd, 'w') as f:
                f.write(code)
            yield temp_file
        finally:
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)
    
    def execute(self, code: str, language: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """Execute code in specified language
        
        Args:
            code: Code to execute
            language: Programming language
            timeout: Execution timeout in seconds
            
        Returns:
            Dictionary with stdout, stderr, exit_code, and execution_time
        """
        timeout = timeout or self.timeout
        
        try:
            ext = self.LANGUAGE_EXTENSIONS.get(language, '.txt')
            cmd = self.LANGUAGE_COMMANDS.get(language)
            
            if not cmd:
                return {
                    'stdout': '',
                    'stderr': f'Unsupported language: {language}',
                    'exit_code': 1,
                    'execution_time': 0,
                }
            
            with self._temp_file(code, ext) as temp_file:
                start_time = time.time()
                
                try:
                    process = subprocess.Popen(
                        f'{cmd} {temp_file}',
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    stdout, stderr = process.communicate(timeout=timeout)
                    execution_time = time.time() - start_time
                    
                    return {
                        'stdout': stdout,
                        'stderr': stderr,
                        'exit_code': process.returncode,
                        'execution_time': execution_time,
                    }
                    
                except subprocess.TimeoutExpired:
                    process.kill()
                    stdout, stderr = process.communicate()
                    return {
                        'stdout': stdout or '',
                        'stderr': f"Timeout after {timeout} seconds\n{stderr or ''}",
                        'exit_code': -1,
                        'execution_time': timeout,
                    }
                    
        except Exception as e:
            logger.error(f"Code execution error: {str(e)}", exc_info=True)
            return {
                'stdout': '',
                'stderr': f'Execution error: {str(e)}',
                'exit_code': 1,
                'execution_time': 0,
            }
    
    def is_language_supported(self, language: str) -> bool:
        """Check if a language is supported for execution
        
        Args:
            language: Programming language name
            
        Returns:
            True if supported, False otherwise
        """
        return language in self.LANGUAGE_COMMANDS
