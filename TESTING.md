# Testing Guide

This document explains how to run tests for the Blink.local project.

## Backend Tests (Django)

### Prerequisites

First, install the test dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### Running Tests

#### Using pytest (recommended)

```bash
cd backend
pytest
```

#### With coverage report

```bash
pytest --cov=apps --cov-report=html
```

Open `htmlcov/index.html` in your browser to view the coverage report.

#### Run specific test file

```bash
pytest apps/api/tests/test_services.py
pytest apps/core/tests/test_models.py
```

#### Run specific test class or function

```bash
pytest apps/api/tests/test_services.py::OllamaServiceTest
pytest apps/api/tests/test_services.py::OllamaServiceTest::test_generate_code_success
```

#### Run tests with verbose output

```bash
pytest -v
```

#### Run tests matching a pattern

```bash
pytest -k "test_create"
pytest -k "project"
```

### Test Structure

```
backend/
├── apps/
│   ├── api/
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_services.py    # Tests for OllamaService, CodeExecutionService
│   │       └── test_views.py       # Tests for API ViewSets
│   └── core/
│       └── tests/
│           ├── __init__.py
│           └── test_models.py      # Tests for Django models
├── pytest.ini                      # Pytest configuration
└── requirements.txt                # Includes test dependencies
```

### Test Categories

1. **Model Tests** (`test_models.py`): Test database models, relationships, and constraints
2. **Service Tests** (`test_services.py`): Test business logic services with mocking
3. **View Tests** (`test_views.py`): Test API endpoints and HTTP responses

### Writing New Tests

Follow this pattern:

```python
from django.test import TestCase
from apps.core.models import Project

class MyModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name='Test')
    
    def test_something(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(...)
```

### Continuous Integration

Tests can be run in CI/CD pipelines:

```yaml
# Example GitHub Actions step
- name: Run tests
  run: |
    cd backend
    pip install -r requirements.txt
    pytest --cov=apps --cov-report=xml
```

## Frontend Tests

### Setup

```bash
npm install
```

### Running Tests

```bash
# Type checking
npm run typecheck

# Linting
npm run lint

# Build (verifies compilation)
npm run build
```

### Adding Frontend Tests

Install testing libraries:

```bash
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom jsdom
```

Add to `vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
  },
})
```

## Best Practices

1. **Write tests first** (TDD) when possible
2. **Mock external services** (Ollama, Supabase)
3. **Use meaningful test names** that describe the behavior
4. **Keep tests independent** - each test should run in isolation
5. **Test edge cases** and error conditions
6. **Maintain good coverage** (>80% recommended)
7. **Run tests before committing**

## Troubleshooting

### Database errors

```bash
# Reset test database
pytest --create-db
```

### Import errors

```bash
# Ensure you're in the backend directory
cd backend
python manage.py check
```

### Slow tests

```bash
# Run only fast tests (exclude slow marker)
pytest -m "not slow"
```
