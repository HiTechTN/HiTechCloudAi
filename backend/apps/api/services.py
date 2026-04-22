import os
import requests
import subprocess
import time
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OllamaService:
    def __init__(self):
        self.base_url = os.getenv('OLLAMA_API_URL', 'http://localhost:11434')
        self.model = 'codellama'

    def generate_code(self, prompt: str, language: str = 'python') -> str:
        try:
            formatted_prompt = f"Generate {language} code for: {prompt}"

            response = requests.post(
                f'{self.base_url}/api/generate',
                json={
                    'model': self.model,
                    'prompt': formatted_prompt,
                    'stream': False,
                },
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            return data.get('response', '')
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API error: {str(e)}")
            raise Exception(f"Failed to generate code with Ollama: {str(e)}")

    def list_models(self) -> list:
        try:
            response = requests.get(f'{self.base_url}/api/tags', timeout=10)
            response.raise_for_status()
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API error: {str(e)}")
            return []


class CodeExecutionService:
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

    def execute(self, code: str, language: str, timeout: int = 30) -> Dict[str, Any]:
        try:
            ext = self.LANGUAGE_EXTENSIONS.get(language, '.txt')
            cmd = self.LANGUAGE_COMMANDS.get(language, 'echo')

            temp_file = f'/tmp/exec_{int(time.time())}{ext}'

            with open(temp_file, 'w') as f:
                f.write(code)

            start_time = time.time()

            process = subprocess.Popen(
                f'{cmd} {temp_file}',
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            try:
                stdout, stderr = process.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                stderr = f"Timeout after {timeout} seconds\n{stderr}"

            execution_time = time.time() - start_time

            os.remove(temp_file)

            return {
                'stdout': stdout,
                'stderr': stderr,
                'exit_code': process.returncode,
                'execution_time': execution_time,
            }
        except Exception as e:
            logger.error(f"Code execution error: {str(e)}")
            return {
                'stdout': '',
                'stderr': str(e),
                'exit_code': 1,
                'execution_time': 0,
            }
