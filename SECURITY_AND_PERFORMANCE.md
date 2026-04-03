# Security Analysis & Performance Optimization

## 🔒 Security Vulnerabilities Found

### 1. **SQL Injection Risk - Low**
**Location**: `backend/apps/api/views.py`
```python
# Current code uses Django ORM which is safe, but be aware of raw SQL
project_id = self.request.query_params.get('project_id')
```
**Status**: ✅ Already protected by Django ORM
**Recommendation**: Continue using ORM methods, avoid raw SQL queries

### 2. **Command Injection - Medium** ⚠️
**Location**: `backend/apps/api/services.py:167`
```python
process = subprocess.Popen(
    f'{cmd} {temp_file}',  # VULNERABLE to shell injection
    shell=True,            # DANGEROUS
    ...
)
```
**Risk**: If language or file path can be manipulated, arbitrary commands could execute
**Fix**:
```python
import shlex
process = subprocess.Popen(
    shlex.split(f'{cmd} {temp_file}'),
    shell=False,  # Disable shell
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
```

### 3. **Missing Input Validation - Medium** ⚠️
**Location**: `backend/apps/api/views.py`
```python
name = request.data.get('name', 'untitled')
path = request.data.get('path', f'untitled_{int(time.time())}.txt')
```
**Risk**: Path traversal attacks (e.g., `../../../etc/passwd`)
**Fix**:
```python
import os
from django.core.exceptions import ValidationError

def validate_path(path):
    if '..' in path or path.startswith('/'):
        raise ValidationError('Invalid path')
    if not os.path.basename(path):
        raise ValidationError('Path must include filename')
    return path
```

### 4. **Missing Authentication - High** ⚠️
**Location**: All API endpoints
```python
permission_classes = [IsAuthenticatedOrReadOnly]
```
**Risk**: Anyone can read data without authentication
**Fix**: Require authentication for all operations in production
```python
permission_classes = [IsAuthenticated]
```

### 5. **CORS Configuration - Medium** ⚠️
**Location**: `backend/project/settings.py`
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5173',
    # ...
]
```
**Risk**: Currently allows localhost only (good for dev), but ensure production has strict origins
**Fix**: Never use `CORS_ALLOW_ALL_ORIGINS = True` in production

### 6. **Secret Key in Code - Low** ⚠️
**Location**: `backend/project/settings.py`
```python
SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-in-production')
```
**Risk**: Default value should never be used
**Fix**: Always set `SECRET_KEY` in environment variables

### 7. **Debug Mode - Medium** ⚠️
**Location**: `backend/project/settings.py`
```python
DEBUG = env('DEBUG', default=False)
```
**Risk**: Ensure DEBUG is False in production
**Fix**: Add check in deployment script

### 8. **Code Execution Without Resource Limits - High** ⚠️
**Location**: `backend/apps/api/services.py`
```python
process = subprocess.Popen(...)
```
**Risk**: Infinite loops, memory exhaustion, CPU abuse
**Fix**:
```python
import resource

def set_limits():
    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))  # 5 seconds
    resource.setrlimit(resource.RLIMIT_AS, (100 * 1024 * 1024,))  # 100MB memory
```

### 9. **Missing Rate Limiting - Medium** ⚠️
**Location**: API endpoints
**Risk**: DoS attacks, brute force
**Fix**: Add django-ratelimit
```bash
pip install django-ratelimit
```

### 10. **Sensitive Data Exposure - Low** ⚠️
**Location**: Error responses
```python
return Response({'error': str(e)}, status=...)
```
**Risk**: Internal error details leaked to users
**Fix**: Log full error, return generic message

---

## ⚡ Performance Optimizations

### 1. **Database Query Optimization** ✅ (Partially Implemented)
**Current**: Uses `prefetch_related` and `select_related`
```python
queryset = Project.objects.prefetch_related(
    Prefetch('files', queryset=File.objects.order_by('path'))
).all()
```
**Additional improvements**:
```python
# Add database indexes
class Meta:
    indexes = [
        models.Index(fields=['-created_at']),
        models.Index(fields=['project', '-created_at']),
    ]
```

### 2. **Caching Strategy** 🔄 (Not Implemented)
**Add Redis caching for frequently accessed data**:
```python
from django.core.cache import cache

def get_project_files(project_id):
    cache_key = f'project_{project_id}_files'
    files = cache.get(cache_key)
    if files is None:
        files = File.objects.filter(project_id=project_id)
        cache.set(cache_key, files, timeout=300)  # 5 minutes
    return files
```

### 3. **API Response Pagination** ✅ (Configured)
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}
```
**Improvement**: Add cursor pagination for large datasets

### 4. **Async Code Execution** 🔄 (Not Implemented)
**Current**: Synchronous code execution blocks requests
**Improvement**: Use Celery for async execution
```python
@shared_task
def execute_code_async(file_id):
    file = File.objects.get(id=file_id)
    result = CodeExecutionService().execute(file.content, file.language)
    return result
```

### 5. **Database Connection Pooling** 🔄 (Not Configured)
**Add to settings.py**:
```python
DATABASES['default']['CONN_MAX_AGE'] = 60  # Persistent connections
DATABASES['default']['OPTIONS'] = {
    'pool_size': 10,
    'max_overflow': 20,
}
```

### 6. **Static File Optimization** 🔄 (Not Configured)
```python
# settings.py
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Middleware (add after SecurityMiddleware)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
```

### 7. **Gunicorn Workers Tuning**
**Current**: Default configuration
**Optimal**: `(2 x CPU cores) + 1` workers
```bash
gunicorn project.wsgi:application --workers 5 --threads 2 --worker-class gthread
```

### 8. **Frontend Bundle Optimization**
**Current**: Development build
**Improvements**:
- Enable code splitting in Vite
- Lazy load components
- Tree shaking
- Compress assets with gzip/brotli

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
        },
      },
    },
  },
})
```

### 9. **Image/Media Optimization** (If applicable)
- Use WebP format
- Implement lazy loading
- CDN for static assets

### 10. **Query Optimization**
**Add select_related/prefetch_related**:
```python
# In views.py
queryset = File.objects.select_related('project').all()
```

---

## 📊 Performance Benchmarks to Track

| Metric | Current | Target |
|--------|---------|--------|
| API Response Time | N/A | < 200ms |
| Database Queries per Request | N/A | < 10 |
| Code Execution Timeout | 30s | 10s |
| Cache Hit Ratio | 0% | > 80% |
| Frontend Load Time | N/A | < 2s |

---

## 🛠️ Action Items

### Immediate (High Priority)
1. [ ] Fix command injection vulnerability (use `shell=False`)
2. [ ] Add input validation for file paths
3. [ ] Set resource limits for code execution
4. [ ] Enable authentication in production

### Short-term (Medium Priority)
5. [ ] Implement rate limiting
6. [ ] Add database indexes
7. [ ] Configure Redis caching
8. [ ] Sanitize error messages

### Long-term (Low Priority)
9. [ ] Migrate to async code execution with Celery
10. [ ] Implement CDN for static assets
11. [ ] Add comprehensive monitoring (Prometheus/Grafana)
12. [ ] Security audit with tools like Bandit, Safety

---

## 🔍 Security Tools Recommended

```bash
# Python security scanning
pip install bandit safety pip-audit
bandit -r backend/
safety check
pip-audit

# Dependency checking
npm audit  # For frontend
```

## 📈 Monitoring Setup

```python
# Add to settings.py
MIDDLEWARE += [
    'django_structlog.middlewares.RequestMiddleware',
]

# Logging configuration
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/app.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```
