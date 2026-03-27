# Blink.local - Local IDE Clone with Docker, Django & Ollama

A complete, production-ready local development environment clone that brings intelligent code generation, multi-language support, and secure external access to your machine.

## Features

- **Modern IDE Interface**: Full-featured code editor with file tree, syntax highlighting
- **AI Code Generation**: Powered by local Ollama instance for generating code snippets
- **Code Execution**: Execute code in isolated Docker containers (Python, JavaScript, Bash, Go, Rust, etc.)
- **VS Code Server**: Full VS Code in browser for advanced editing
- **Cloudflare Tunnel**: Secure external access without opening ports
- **Supabase Integration**: Cloud database for persistent storage
- **Real-time Collaboration**: WebSocket support for live updates
- **Docker Compose Orchestration**: One-command deployment

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Cloudflare Tunnel                         │
│                (Secure external access)                      │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                   Nginx Reverse Proxy                        │
│              (Route to services, CORS, SSL)                  │
└─────────────────────────────────────────────────────────────┘
       ↓                    ↓                    ↓
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Frontend   │   │  Django API  │   │ Code-Server  │
│   (React)    │   │  (DRF)       │   │ (VS Code)    │
└──────────────┘   └──────────────┘   └──────────────┘
       ↓                    ↓                    ↓
   Vite Dev           Django/Gunicorn      Code-Server
   Server             + Channels           Container
                           ↓
                    ┌──────────────┐
                    │   Supabase   │
                    │  PostgreSQL  │
                    └──────────────┘
                           ↓
                    ┌──────────────┐
                    │    Redis     │
                    │   Cache      │
                    └──────────────┘
                           ↓
                    ┌──────────────┐
                    │    Ollama    │
                    │  AI Models   │
                    └──────────────┘
```

## Prerequisites

### Required
- Docker & Docker Compose (v1.29+)
- 8GB RAM minimum (16GB recommended)
- 50GB disk space
- Supabase account with database credentials

### Optional
- Cloudflare account for tunnel access
- Ollama installed (or will use Docker image)

## Installation

### 1. Clone and Setup

```bash
git clone <repository>
cd blink-local
mkdir -p shared_data
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with:
```
# Django
DJANGO_SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,nginx

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_DB_URL=postgresql://user:password@your-project.supabase.co:5432/postgres

# Redis
REDIS_URL=redis://redis:6379/0

# Ollama
OLLAMA_API_URL=http://ollama:11434

# Code Server
CODE_SERVER_PASSWORD=your-secure-password

# Cloudflare (Optional)
CLOUDFLARE_TUNNEL_TOKEN=your-tunnel-token
```

### 3. Start Services

Quick start:
```bash
bash scripts/start.sh
```

Or manually:
```bash
docker-compose up -d
```

Check status:
```bash
docker-compose ps
docker-compose logs -f
```

## Usage

### Accessing the IDE

**Local Access:**
- Frontend: http://localhost (via Nginx)
- API: http://localhost/api/
- Code-Server: http://localhost/code-server/

**Direct Access:**
- Frontend: http://localhost:5173 (Vite)
- API: http://localhost:8000
- Code-Server: https://localhost:8443

### Creating a Project

1. Click "New Project" button
2. Enter project name
3. Start creating files

### Creating Files

1. Click the "+" button in the file tree
2. Files are automatically saved to Supabase
3. View file history in the project dashboard

### Writing Code

1. Select a file to edit
2. Write code in the editor
3. Press Ctrl+S or click Save
4. Click Play button to execute

### AI Code Generation

1. Open the AI Panel (right sidebar)
2. Select target language
3. Describe what code you need
4. Click "Generate"
5. Click "Insert" to add generated code to your file

### Managing Files

- **Save**: Ctrl+S or Save button
- **Execute**: Play button or Ctrl+Enter
- **Delete**: Trash button
- **Copy**: Copy button in toolbar

## Cloudflare Tunnel Setup

For secure external access without port forwarding:

### 1. Prerequisites
- Cloudflare account
- Domain managed by Cloudflare
- `cloudflared` CLI installed

### 2. Run Setup Script

```bash
bash scripts/setup-cloudflare.sh
```

This will:
1. Authenticate with Cloudflare
2. Create a tunnel
3. Generate tunnel token
4. Provide configuration instructions

### 3. Add Tunnel Token

```bash
# Update .env
echo "CLOUDFLARE_TUNNEL_TOKEN=<your-token>" >> .env

# Restart Docker Compose
docker-compose restart cloudflare-tunnel
```

### 4. Access Remotely

Your app will be available at:
```
https://blink.yourdomain.com
```

## API Endpoints

### Projects
```bash
GET    /api/projects/              # List all projects
POST   /api/projects/              # Create project
GET    /api/projects/{id}/         # Get project
PUT    /api/projects/{id}/         # Update project
DELETE /api/projects/{id}/         # Delete project
GET    /api/projects/{id}/files/   # List project files
POST   /api/projects/{id}/create_file/ # Create file
```

### Files
```bash
GET    /api/files/                 # List all files
POST   /api/files/                 # Create file
GET    /api/files/{id}/            # Get file
PUT    /api/files/{id}/            # Update file
DELETE /api/files/{id}/            # Delete file
POST   /api/files/{id}/execute/    # Execute file
GET    /api/files/by_project/      # List files by project
```

### Code Generation
```bash
POST   /api/generations/generate/  # Generate code
GET    /api/generations/           # List generations
GET    /api/generations/by_project/ # Get generations by project
```

### Sessions
```bash
GET    /api/sessions/              # List sessions
POST   /api/sessions/              # Create session
GET    /api/sessions/{id}/         # Get session
PUT    /api/sessions/{id}/         # Update session
PATCH  /api/sessions/{id}/update_cursor/ # Update cursor position
```

## Environment Variables

### Core
- `DJANGO_SECRET_KEY`: Secret key for Django (change in production!)
- `DEBUG`: Debug mode (False in production)
- `ALLOWED_HOSTS`: Comma-separated allowed hosts

### Supabase
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_ANON_KEY`: Public API key
- `SUPABASE_SERVICE_ROLE_KEY`: Service role key (secret!)
- `SUPABASE_DB_URL`: Direct PostgreSQL connection

### Services
- `REDIS_URL`: Redis connection URL
- `OLLAMA_API_URL`: Ollama API endpoint
- `CODE_SERVER_PASSWORD`: Password for Code-Server

### Cloudflare
- `CLOUDFLARE_TUNNEL_TOKEN`: Tunnel authentication token

## Docker Services

### Backend
- Django REST API
- Gunicorn WSGI server
- Channels for WebSockets
- Health check every 30s

### Frontend
- React with Vite
- Hot module replacement
- Built-in API client
- TypeScript support

### Code-Server
- VS Code in browser
- Full extension support
- Configurable settings
- Password protected

### Redis
- Session caching
- Real-time updates
- Job queue support

### Nginx
- Reverse proxy
- Load balancing
- SSL/TLS termination
- CORS handling

### Ollama
- Local LLM inference
- Multiple model support
- GPU acceleration (if available)

### Cloudflare Tunnel
- Secure external access
- No port forwarding needed
- DDoS protection
- SSL/TLS encryption

## Monitoring & Logs

### View All Logs
```bash
docker-compose logs -f
```

### View Specific Service
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx
```

### Check Service Health
```bash
docker-compose ps
docker stats
```

## Database

### Supabase Tables

#### projects
```sql
- id (UUID, PK)
- name (TEXT)
- description (TEXT)
- created_at (TIMESTAMPTZ)
- updated_at (TIMESTAMPTZ)
```

#### files
```sql
- id (UUID, PK)
- project_id (UUID, FK)
- name (TEXT)
- path (TEXT)
- content (TEXT)
- language (TEXT)
- created_at (TIMESTAMPTZ)
- updated_at (TIMESTAMPTZ)
```

#### code_generations
```sql
- id (UUID, PK)
- project_id (UUID, FK)
- prompt (TEXT)
- generated_code (TEXT)
- language (TEXT)
- model_used (TEXT)
- created_at (TIMESTAMPTZ)
```

#### execution_results
```sql
- id (UUID, PK)
- file_id (UUID, FK)
- language (TEXT)
- stdout (TEXT)
- stderr (TEXT)
- exit_code (INT)
- execution_time (FLOAT)
- created_at (TIMESTAMPTZ)
```

#### sessions
```sql
- id (UUID, PK)
- project_id (UUID, FK)
- name (TEXT)
- active_file_id (UUID, FK)
- cursor_position (INT)
- created_at (TIMESTAMPTZ)
- updated_at (TIMESTAMPTZ)
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port in docker-compose.yml
```

### Ollama Connection Failed
```bash
# Check if Ollama is running
docker-compose logs ollama

# Pull a model
docker-compose exec ollama ollama pull codellama

# Test API
curl http://localhost:11434/api/tags
```

### Database Connection Error
```bash
# Check Supabase credentials in .env
# Test connection:
psql "postgresql://user:password@host:5432/postgres"

# Verify RLS policies are not blocking access
```

### Frontend Not Loading
```bash
# Clear frontend cache
docker-compose restart frontend

# Check Vite server
docker-compose logs frontend
```

### Code Execution Timeout
- Increase timeout in `backend/apps/api/services.py`
- Check resource limits in `docker-compose.yml`
- Monitor with `docker stats`

## Performance Tuning

### Django
- Increase workers in Dockerfile: `--workers 8`
- Adjust timeout: `--timeout 120`

### Redis
- Increase memory: Change `docker-compose.yml`
- Use persistence: Add `appendonly yes` to config

### Ollama
- Use smaller models for faster inference
- Enable GPU acceleration if available
- Set `OLLAMA_NUM_PARALLEL=4` for parallelism

### Frontend
- Enable production builds: `npm run build`
- Use CDN for static assets
- Enable compression in Nginx

## Security Best Practices

### In Development
- Keep `DEBUG=False` when possible
- Use strong `DJANGO_SECRET_KEY`
- Restrict `ALLOWED_HOSTS`
- Use HTTPS in production

### Cloudflare Tunnel
- Keep tunnel token secret
- Rotate tokens regularly
- Enable WAF rules
- Use authentication policies

### Database
- Use strong passwords
- Enable SSL connections
- Restrict IP access in Supabase
- Regular backups

### Code Execution
- Disable dangerous commands in sandbox
- Set resource limits
- Monitor execution logs
- Implement rate limiting

## Deployment

### Production Checklist
- [ ] Change `DJANGO_SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure real domain in Cloudflare
- [ ] Enable HTTPS
- [ ] Set up SSL certificates
- [ ] Configure backups for Supabase
- [ ] Enable monitoring/logging
- [ ] Set resource limits
- [ ] Configure firewall rules
- [ ] Enable rate limiting

### Docker Registry Push
```bash
docker tag blink-backend:latest your-registry/blink-backend:latest
docker push your-registry/blink-backend:latest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with Docker Compose
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
1. Check troubleshooting section
2. Review logs: `docker-compose logs`
3. Check database with Supabase console
4. Inspect network with browser DevTools

---

**Built with ❤️ for developers who want their own local IDE**
