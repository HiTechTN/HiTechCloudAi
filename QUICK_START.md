# Blink.local - Quick Start Guide

## 60 Second Setup

### 1. Get Supabase Credentials (2 minutes)

Visit https://supabase.com and:
1. Click "New Project"
2. Fill in project name
3. Wait for project to initialize
4. Go to Settings > API
5. Copy these 3 values:
   - **Project URL** → `SUPABASE_URL`
   - **Anon key** → `SUPABASE_ANON_KEY`
   - **Service role key** → `SUPABASE_SERVICE_ROLE_KEY`
6. Go to Settings > Database and get connection string → `SUPABASE_DB_URL`

### 2. Configure Environment (1 minute)

```bash
# Edit your .env file
nano .env
```

Update these 4 variables:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJ0eXAi...
SUPABASE_SERVICE_ROLE_KEY=eyJ0eXAi...
SUPABASE_DB_URL=postgresql://postgres:password@...
```

### 3. Start Everything (1 minute)

```bash
bash scripts/start.sh
```

### 4. Open IDE (10 seconds)

```
http://localhost
```

---

## What You Get

```
Frontend IDE       → http://localhost
↓
Django API        → http://localhost/api/
↓
PostgreSQL        → Supabase Cloud
↓
AI Code Gen       → Ollama Local
↓
Code Execution    → Isolated Docker
```

## First Project

1. **Create Project**
   - Click "New Project" button
   - Name: "Hello World"
   - Click Create

2. **Create File**
   - Click "+" in file tree
   - Creates `untitled.py`

3. **Write Code**
   ```python
   print("Hello from Blink.local!")
   ```

4. **Save**
   - Ctrl+S or Save button

5. **Execute**
   - Play button
   - See output below

6. **Generate with AI**
   - Open AI Panel (right side)
   - Prompt: "Create a function to reverse a string"
   - Click Generate
   - Click Insert

---

## Architecture Overview

```
┌─ Frontend (React) ─────────────────┐
│  - File Tree                       │
│  - Code Editor                     │
│  - Output Terminal                 │
│  - AI Assistant                    │
└────────────┬────────────────────────┘
             │ HTTP API
             ↓
┌─ Backend (Django) ─────────────────┐
│  - Project Management              │
│  - File CRUD                       │
│  - Code Execution                  │
│  - Ollama Integration              │
└────────────┬────────────────────────┘
             │ PostgreSQL
             ↓
┌─ Database (Supabase) ──────────────┐
│  - Projects Table                  │
│  - Files Table                     │
│  - Generations Table               │
│  - Execution Results               │
└────────────────────────────────────┘

Additional Services:
- Redis: Caching & Sessions
- Ollama: AI Code Generation
- Code-Server: VS Code in Browser
- Nginx: Reverse Proxy & Routing
- Cloudflare: External Access
```

---

## Directory Structure

```
blink-local/
├── src/                         # Frontend React
│   ├── App.tsx                  # Main IDE component
│   ├── components/              # UI components
│   │   ├── Editor.tsx           # Code editor
│   │   ├── FileTree.tsx         # File browser
│   │   ├── OutputPanel.tsx      # Terminal output
│   │   └── AIPanel.tsx          # AI assistant
│   ├── services/                # API client
│   └── types/                   # TypeScript types
│
├── backend/                     # Django Backend
│   ├── project/                 # Django config
│   │   ├── settings.py          # Configuration
│   │   ├── urls.py              # URL routing
│   │   └── wsgi.py              # WSGI app
│   ├── apps/                    # Django apps
│   │   ├── core/                # Models
│   │   └── api/                 # API views
│   ├── Dockerfile
│   └── requirements.txt          # Python dependencies
│
├── nginx/                       # Reverse Proxy
│   ├── Dockerfile
│   └── nginx.conf               # Nginx configuration
│
├── code-server-config/          # VS Code Settings
├── scripts/                     # Helper scripts
│   ├── start.sh                 # Start all services
│   ├── setup-cloudflare.sh      # Tunnel setup
│   └── validate.sh              # Project validation
│
├── docker-compose.yml           # Service orchestration
├── README.md                    # Full documentation
├── BLINK_SETUP.md              # Detailed setup
└── Makefile                     # Useful commands
```

---

## Common Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Access database
psql "postgresql://..."

# Execute code in backend
docker-compose exec backend python manage.py shell

# View file tree
ls -la backend/

# Make script executable
chmod +x scripts/start.sh
```

---

## Supported Languages

✓ Python
✓ JavaScript
✓ TypeScript
✓ Bash
✓ Go
✓ Rust
✓ Java (partial)

Add more by editing `backend/apps/api/services.py`

---

## Troubleshooting

### "Connection refused"
```bash
# Services not started?
docker-compose ps

# Start them:
docker-compose up -d
```

### "Permission denied"
```bash
# Make scripts executable:
chmod +x scripts/*.sh
```

### "Database error"
- Check `.env` credentials match your Supabase project
- Visit Supabase console: https://app.supabase.com

### "Port already in use"
```bash
# Find what's using it:
lsof -i :8000

# Change port in docker-compose.yml
```

### "Container won't build"
```bash
# Rebuild from scratch:
docker-compose build --no-cache
```

---

## Next Steps

1. **Explore the IDE**
   - Create projects
   - Write and execute code
   - Generate code with AI

2. **Learn the API**
   - Visit: http://localhost:8000/api/
   - Try endpoints with curl/Postman

3. **Use Code-Server**
   - Open: http://localhost:8443
   - Full VS Code in browser

4. **Setup External Access**
   - Run: `bash scripts/setup-cloudflare.sh`
   - Access from anywhere

5. **Read Full Docs**
   - See: `README.md`
   - Advanced: `BLINK_SETUP.md`

---

## Tips & Tricks

### Keyboard Shortcuts
- **Ctrl+S** - Save file
- **Ctrl+Enter** - Execute code
- **Ctrl+Shift+P** - Command palette (in Code-Server)

### Quick Project Management
```bash
# Use Makefile for common tasks
make start              # Start all
make logs               # View logs
make stop               # Stop all
make clean              # Remove everything
make tunnel             # Setup Cloudflare
```

### Development Mode
```bash
# Keep services running while developing
docker-compose logs -f

# In another terminal, edit code
nano src/App.tsx

# Changes auto-reload in browser
```

### Pull Ollama Models
```bash
docker-compose exec ollama ollama pull mistral
docker-compose exec ollama ollama list
```

---

## Performance

For best experience:
- **RAM**: 8GB minimum, 16GB+ recommended
- **CPU**: 2 cores minimum, 4+ recommended
- **Disk**: 50GB minimum, 100GB+ recommended
- **GPU**: Optional, speeds up Ollama inference

Monitor with:
```bash
docker stats
```

---

## Production Deployment

### AWS EC2
```bash
# SSH into instance
ssh -i key.pem ubuntu@your-instance

# Install Docker
sudo apt update && sudo apt install docker.io docker-compose

# Clone and run
git clone <your-repo>
cd blink-local
bash scripts/start.sh
```

### DigitalOcean
- Create Droplet with Docker pre-installed
- SSH and follow above steps

### Your Home Server
- Install Docker
- Run with Cloudflare Tunnel (no port forwarding needed!)

---

## What's Running

When you start Blink:

| Service | Port | Purpose |
|---------|------|---------|
| Nginx | 80 | Reverse proxy |
| Frontend | 5173 | React Vite dev server |
| Backend | 8000 | Django API |
| Code-Server | 8443 | VS Code in browser |
| Redis | 6379 | Caching |
| Ollama | 11434 | AI inference |
| PostgreSQL | 5432 | Supabase cloud |

All routed through Nginx at `http://localhost`

---

## Security Notes

- **.env is secret!** Don't commit it
- Change `DJANGO_SECRET_KEY` in production
- Use HTTPS with Cloudflare Tunnel
- Keep Docker images updated
- Enable Supabase RLS policies

---

## Need Help?

1. **Check logs**: `docker-compose logs`
2. **Read docs**: `README.md`
3. **Validate setup**: `bash scripts/validate.sh`
4. **Inspect database**: https://app.supabase.com
5. **Test API**: `curl http://localhost:8000/api/health/`

---

## You're All Set!

```
Open http://localhost and start coding!
```

Enjoy your local Blink clone! 🚀

Questions? Check README.md or BLINK_SETUP.md
