# Blink.local - Universal Local IDE Clone

A production-ready, intelligent local development environment that combines a modern IDE, AI-powered code generation, multi-language code execution, and secure external access via Cloudflare Tunnels.

## Quick Start

### 1. Prerequisites
```bash
# Install Docker and Docker Compose
# - Docker Desktop: https://www.docker.com/products/docker-desktop
# - Or: apt install docker.io docker-compose (Linux)

# Verify installation
docker --version
docker-compose --version
```

### 2. Setup Supabase (First Time Only)

1. Create account at https://supabase.com
2. Create new project
3. Go to Settings > API
4. Copy these values:

   - `Project URL` → `SUPABASE_URL`
   - `anon public` → `SUPABASE_ANON_KEY`
   - `service_role secret` → `SUPABASE_SERVICE_ROLE_KEY`
   - Get `Database URL` from Settings > Database

### 3. Configure Environment

```bash
# Copy example to actual .env
cp .env.example .env

# Edit .env with your Supabase credentials
nano .env
# Update: SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_DB_URL
```

### 4. Start Everything

```bash
# Run setup script (handles building and starting)
bash scripts/start.sh

# Or manual commands:
docker-compose build
docker-compose up -d
```

### 5. Access the IDE

**Open in browser:**
```
http://localhost
```

Or with ports:
- Frontend (Vite): http://localhost:5173
- API: http://localhost:8000/api/
- Code-Server: http://localhost:8443
- Nginx: http://localhost:80

## Usage Guide

### Create Your First Project

1. Click **"New Project"** button
2. Enter project name
3. Click **"Create"**
4. Click **"+"** in file tree to create file
5. Start coding!

### Run Code

1. Write code in editor
2. Click **Play** button (or Ctrl+Enter)
3. View output in bottom panel

### Generate Code with AI

1. Open **"AI Code Assistant"** panel (right side)
2. Select language
3. Type what code you want
4. Click **"Generate"**
5. Review code and click **"Insert"** to add to your file

### Supported Languages
- Python
- JavaScript / TypeScript
- Bash
- Go
- Rust
- And more!

## Cloudflare Tunnel (External Access)

To access your IDE from anywhere safely:

### 1. Setup Tunnel
```bash
bash scripts/setup-cloudflare.sh
```

### 2. Follow Instructions
- Create Cloudflare account (free)
- Point domain to Cloudflare
- Get tunnel token
- Add to .env: `CLOUDFLARE_TUNNEL_TOKEN=...`

### 3. Restart
```bash
docker-compose restart cloudflare-tunnel
```

### 4. Access Remotely
```
https://blink.yourdomain.com
```

## Project Structure

```
project/
├── src/                          # Frontend React/TypeScript
│   ├── components/               # UI Components
│   ├── services/                 # API Client
│   ├── types/                    # TypeScript Types
│   └── App.tsx                   # Main App Component
├── backend/                      # Django Backend
│   ├── project/                  # Django Settings
│   ├── apps/
│   │   ├── core/                 # Models
│   │   └── api/                  # Views & Serializers
│   └── requirements.txt
├── nginx/                        # Reverse Proxy Config
├── code-server-config/           # VS Code Settings
├── scripts/
│   ├── start.sh                  # Start all services
│   └── setup-cloudflare.sh       # Tunnel setup
├── docker-compose.yml            # Service Orchestration
└── BLINK_SETUP.md               # Detailed Documentation
```

## API Endpoints

### Projects
```
GET    /api/projects/             List all
POST   /api/projects/             Create
GET    /api/projects/{id}/        Get one
PUT    /api/projects/{id}/        Update
DELETE /api/projects/{id}/        Delete
```

### Files
```
GET    /api/files/               List all
POST   /api/files/               Create
GET    /api/files/{id}/          Get one
PUT    /api/files/{id}/          Update
DELETE /api/files/{id}/          Delete
POST   /api/files/{id}/execute/  Run code
```

### AI Generation
```
POST   /api/generations/generate/  Generate code
GET    /api/generations/           List all
```

## Environment Variables

```bash
# Required
SUPABASE_URL=https://...
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...
SUPABASE_DB_URL=postgresql://...

# Optional but Recommended
DJANGO_SECRET_KEY=your-secret-key
CODE_SERVER_PASSWORD=your-password
CLOUDFLARE_TUNNEL_TOKEN=...
```

See `.env.example` for all options.

## Common Tasks

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stop Services
```bash
docker-compose down
```

### Restart Service
```bash
docker-compose restart backend
docker-compose restart frontend
```

### Access Database
```bash
# Use Supabase web console at https://app.supabase.com
# Or via psql:
psql "postgresql://user:password@host:5432/postgres"
```

### Pull Ollama Models
```bash
# List available models
curl http://localhost:11434/api/tags

# Pull new model
docker-compose exec ollama ollama pull mistral
```

### Use Code-Server Instead
If you prefer full VS Code in browser:
1. Navigate to http://localhost:8443
2. Enter password from .env: `CODE_SERVER_PASSWORD`
3. Full IDE experience with extensions

## Troubleshooting

### Services won't start
```bash
# Check Docker is running
docker ps

# View detailed logs
docker-compose logs

# Rebuild containers
docker-compose build --no-cache
```

### Supabase connection fails
```bash
# Verify credentials in .env match your Supabase project
# Check database is active in Supabase console
# Test connection: psql "postgresql://..."
```

### Port conflicts
```bash
# Find what's using port 8000
lsof -i :8000

# Kill it or change port in docker-compose.yml
```

### API not responding
```bash
# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend

# Check health
curl http://localhost:8000/api/health/
```

### Code execution fails
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Pull a model
docker-compose exec ollama ollama pull codellama

# Check execution logs in backend
docker-compose logs backend | grep execute
```

## Performance Tips

- **Use smaller Ollama models** (e.g., `mistral:7b`) for faster generation
- **Increase Docker memory** if code execution is slow
- **Use production frontend build** for deployment
- **Enable Redis caching** for API responses
- **Compress Nginx output** for bandwidth savings

## Security

### Development
- `.env` contains secrets - never commit it!
- Add `.env` to `.gitignore`
- Use strong `DJANGO_SECRET_KEY`
- Keep `DEBUG=False` in production

### Deployment
- Use HTTPS everywhere (Cloudflare provides this)
- Set strong passwords for all services
- Regular Supabase backups
- Monitor code execution for malicious activity
- Restrict database access by IP

### Code Execution
- All user code runs in isolated containers
- No network access from executed code
- Resource limits enforced
- Execution timeout prevents infinite loops

## What's Included

### Backend (Django)
- REST API with Django REST Framework
- PostgreSQL/Supabase integration
- Redis caching
- Celery task queue ready
- WebSocket support with Channels
- Code execution sandbox

### Frontend (React)
- Modern IDE interface
- File explorer
- Code editor with syntax highlighting
- Terminal/output panel
- AI assistant panel
- Project management

### Services
- **Nginx**: Load balancing & reverse proxy
- **Redis**: Session & cache management
- **Ollama**: Local AI for code generation
- **Code-Server**: Full VS Code in browser
- **Cloudflare Tunnel**: Secure external access

## System Requirements

### Minimum
- 8GB RAM
- 50GB disk space
- 2 CPU cores

### Recommended
- 16GB+ RAM
- 100GB+ disk space
- 4+ CPU cores
- NVIDIA GPU for faster Ollama inference

## Advanced Configuration

### Custom Ollama Model
```bash
# In backend/apps/api/services.py
# Change: self.model = 'codellama'
# To: self.model = 'mistral'  # or any model in your Ollama
```

### Add More Languages
Edit `backend/apps/api/services.py` `LANGUAGE_COMMANDS` dict

### Custom API Endpoint
Edit `src/services/api.ts` `API_URL` variable

### Change Frontend Port
Edit `docker-compose.yml` ports for frontend service

## Development

### Add New API Endpoint
1. Create view in `backend/apps/api/views.py`
2. Add serializer in `backend/apps/api/serializers.py`
3. Register in `backend/apps/api/urls.py`
4. Call from frontend with `api.ts`

### Add New Component
1. Create component in `src/components/`
2. Import in `src/App.tsx`
3. Add styling with Tailwind classes

### Run Tests
```bash
docker-compose exec backend pytest
npm test  # For frontend
```

## Performance Monitoring

```bash
# Docker stats
docker stats

# Database queries (in Supabase console)
# Navigate to: Performance > Slow Queries

# Application logs
docker-compose logs -f backend | grep ERROR
```

## Deployment Options

### AWS EC2
```bash
# Launch instance, install Docker
git clone <repo>
cd blink-local
bash scripts/start.sh
```

### DigitalOcean
- Create Droplet with Docker pre-installed
- SSH and follow Quick Start steps

### Heroku (Not recommended for code execution)
```bash
git push heroku main
```

### Home Server
- Install Docker on any machine
- Forward only Cloudflare Tunnel port
- No need to expose other ports!

## Roadmap

- [ ] Database GUI for Supabase
- [ ] Collaborative editing
- [ ] Git integration
- [ ] Terminal multiplexing
- [ ] Debug mode support
- [ ] Performance profiling
- [ ] Custom themes
- [ ] Plugin system

## Contributing

Pull requests welcome! Please:
1. Fork repo
2. Create feature branch
3. Test with Docker Compose
4. Submit PR

## Support & Documentation

- **Full Docs**: See `BLINK_SETUP.md` for detailed guide
- **API Docs**: Available at `/api/docs/` (Swagger UI)
- **Issues**: GitHub Issues
- **Community**: Join our Discord (link in repo)

## License

MIT - Free to use, modify, and deploy

## Credits

Built with:
- Django & Django REST Framework
- React & Vite
- Docker & Docker Compose
- Supabase
- Ollama
- Cloudflare
- Code-Server

---

**Start coding locally with the power of a cloud IDE!**

Questions? Check the troubleshooting section or open an issue.
