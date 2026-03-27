# Blink.local - START HERE 🚀

Welcome! You have a complete, production-ready local IDE clone. Let's get it running in 5 minutes.

---

## 🎯 What You Have

A complete development environment with:
- Modern code editor in your browser
- AI code generation (Ollama)
- Code execution in isolated containers
- Database with Supabase
- VS Code in browser (Code-Server)
- Secure external access (Cloudflare Tunnel)

Everything is configured and ready to go!

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Get Supabase Credentials (2 min)

Go to https://supabase.com

1. Click "New Project"
2. Wait for it to initialize
3. Go to **Settings > API**
4. Copy these 3 values:
   - `Project URL` → `SUPABASE_URL`
   - `Anon key` → `SUPABASE_ANON_KEY`
   - `Service role key` → `SUPABASE_SERVICE_ROLE_KEY`
5. Also get the database URL from **Settings > Database**

### Step 2: Update Configuration (1 min)

```bash
# Edit your .env file
nano .env
```

Find these lines and paste your Supabase values:
```
SUPABASE_URL=paste-your-url-here
SUPABASE_ANON_KEY=paste-your-key-here
SUPABASE_SERVICE_ROLE_KEY=paste-your-key-here
SUPABASE_DB_URL=paste-your-database-url-here
```

Save and close (Ctrl+X, then Y, then Enter if using nano)

### Step 3: Start Services (1 min)

```bash
bash scripts/start.sh
```

Wait for services to start (about 30 seconds). You'll see:
```
✓ backend is running
✓ frontend is running
✓ nginx is running
✓ redis is running
✓ code-server is running
```

### Step 4: Open IDE (10 seconds)

Open your browser and go to:
```
http://localhost
```

That's it! You're running Blink.local!

---

## 📝 Your First Project

1. **Create a Project**
   - Click "New Project" button (top-left)
   - Name: "Hello World"
   - Click "Create"

2. **Create a File**
   - Click "+" button in file tree (left side)
   - You now have an `untitled.py` file

3. **Write Code**
   ```python
   print("Hello from Blink.local!")
   for i in range(5):
       print(f"Line {i}")
   ```

4. **Save & Execute**
   - Press Ctrl+S to save
   - Click Play button (or Ctrl+Enter)
   - See output in bottom panel!

5. **Generate with AI**
   - Look at right panel: "AI Code Assistant"
   - Type: "Write a function to reverse a string in Python"
   - Click "Generate"
   - Click "Insert" to add to your file

Congratulations! You just used Blink.local! 🎉

---

## 🔗 Access Everything

### Local (Recommended for now)
- IDE: http://localhost
- API: http://localhost:8000/api/
- Code-Server: http://localhost:8443
- Logs: `docker-compose logs -f`

### Direct Ports (if Nginx not working)
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Code-Server: https://localhost:8443

### From Anywhere (After setup)
- Requires: Setup Cloudflare Tunnel
- See: CLOUDFLARE_TUNNEL.md
- Access: https://blink.yourdomain.com

---

## 🛠️ Common Tasks

### View Live Logs
```bash
docker-compose logs -f
```

### Stop Services
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose up -d
```

### Using Make Commands
```bash
make start          # Start all
make logs           # View logs
make stop           # Stop all
make status         # Check status
make tunnel         # Setup Cloudflare
```

### Database Access
Open https://app.supabase.com → Your project → Check your data

### Execute Terminal Commands
In Code-Server (http://localhost:8443), open terminal for full shell access

---

## 📚 Documentation

Start with what you need:

**Just want to use it:**
→ This file (done!) + Experiment

**Want to understand everything:**
→ Read QUICK_START.md (5 min overview)

**Need complete reference:**
→ Read BLINK_SETUP.md (detailed guide)

**Want external access:**
→ Read CLOUDFLARE_TUNNEL.md (tunneling guide)

**Understanding the code:**
→ Read PROJECT_SUMMARY.md (architecture)

**Find something specific:**
→ Use DOCUMENTATION_INDEX.md (navigation)

---

## ⚙️ What's Running

```
Your Machine:
├─ Frontend (React)     → UI in browser
├─ Backend (Django)     → REST API
├─ Code-Server         → VS Code in browser
├─ Nginx              → Routes traffic
├─ Redis              → Caching
├─ Ollama             → AI generation
└─ PostgreSQL (Cloud) → Supabase

Everything connected & ready!
```

---

## 🐛 If Something Doesn't Work

### Services won't start
```bash
# Check Docker is running
docker ps

# See what's wrong
docker-compose logs
```

### Can't see the IDE
```bash
# Check services
docker-compose ps

# All should say "Up"
# If not: docker-compose restart
```

### API errors
```bash
# Test API health
curl http://localhost:8000/api/health/

# View backend logs
docker-compose logs backend
```

### Database errors
- Check .env file has correct Supabase credentials
- Visit https://app.supabase.com and verify project exists
- Check database is in "Running" state

### Port conflicts
```bash
# See what's using ports
lsof -i :8000
lsof -i :5173

# Change ports in docker-compose.yml if needed
```

**More help:** See README.md Troubleshooting section

---

## 🚀 Next Steps

### Learning Path
1. **Create projects** and write code
2. **Try AI generation** - it's amazing!
3. **Execute different languages** - Python, JavaScript, etc.
4. **Use Code-Server** - Full VS Code experience
5. **Setup external access** - Use Cloudflare Tunnel
6. **Deploy somewhere** - AWS, DigitalOcean, etc.

### Extending It
The project is completely customizable:
- Add more languages
- Create custom components
- Integrate with other tools
- Build features you need

See PROJECT_SUMMARY.md for architecture.

---

## 💡 Pro Tips

### Keyboard Shortcuts
```
Ctrl+S           → Save file
Ctrl+Enter       → Execute code
Ctrl+Shift+P     → Command palette (Code-Server)
```

### Using Multiple Files
1. Create multiple files in project
2. Click to switch between them
3. Each saves to database automatically

### Different Languages
1. Choose language in file extension (.py, .js, etc.)
2. Code editor auto-detects
3. AI panel lets you choose language for generation

### Viewing Output
1. Run code with Play button
2. Output appears in bottom panel
3. Shows stdout, stderr, exit code, execution time

### Code-Server Alternative
If you prefer VS Code experience:
1. Open http://localhost:8443
2. Login with password from .env
3. Full IDE with extensions
4. Sync files with main editor

---

## 🔒 Security Notes

### Keep Secret
- Don't share `.env` file
- Don't commit `.env` to git
- Regenerate `DJANGO_SECRET_KEY` for production

### For External Access
- Change `CODE_SERVER_PASSWORD` to something strong
- Use Cloudflare Tunnel (no port forwarding)
- Keep Cloudflare tunnel token secret

### Code Execution
- Code runs in isolated Docker containers
- Limited resources (timeout, memory)
- Safe for untrusted code

---

## ❓ Common Questions

**Q: Can I use this offline?**
A: Yes! Everything runs locally. Only Supabase needs internet. (But you can use local PostgreSQL instead)

**Q: Is my code private?**
A: Yes! Everything runs on your machine. Nothing uploaded unless you use Supabase cloud.

**Q: Can I share with others?**
A: Yes! Use Cloudflare Tunnel (see CLOUDFLARE_TUNNEL.md) to share the URL.

**Q: How do I backup my work?**
A: Supabase auto-backs up. You can also export from dashboard.

**Q: What if I want to modify it?**
A: Go ahead! Read PROJECT_SUMMARY.md to understand the structure.

**Q: Can I deploy it?**
A: Yes! Works on AWS, DigitalOcean, home server, anywhere with Docker.

**Q: What about the AI generation?**
A: Uses local Ollama. Fast, private, no API keys needed.

---

## 📞 Getting Help

1. **Can't get started?** → Check this file again
2. **Need overview?** → Read QUICK_START.md
3. **Want details?** → Read BLINK_SETUP.md
4. **External access?** → Read CLOUDFLARE_TUNNEL.md
5. **Understanding code?** → Read PROJECT_SUMMARY.md
6. **Finding something?** → Use DOCUMENTATION_INDEX.md

---

## 🎓 Learning Resources

### Understanding The Stack
- React: https://react.dev
- Django: https://www.djangoproject.com
- Supabase: https://supabase.com/docs
- Docker: https://docs.docker.com
- Ollama: https://ollama.ai
- Cloudflare: https://developers.cloudflare.com

### Code
- Check inline comments in source files
- Look at example API calls in src/services/api.ts
- Study models in backend/apps/core/models.py

---

## ✅ Checklist

You're all set when:
- [ ] .env file updated with Supabase credentials
- [ ] Services started (`bash scripts/start.sh`)
- [ ] Browser loads http://localhost
- [ ] Created test project
- [ ] Executed some code
- [ ] Generated code with AI

Once all checked, you're ready to build with Blink.local!

---

## 🎉 You're Ready!

Blink.local is installed, configured, and running!

**Open http://localhost and start coding!**

---

## 📖 Documentation Map

```
START_HERE.md (you are here)
    ↓
QUICK_START.md (5-min overview)
    ↓
README.md (common tasks)
    ↓
BLINK_SETUP.md (deep dive)
    ↓
PROJECT_SUMMARY.md (architecture)
    ↓
CLOUDFLARE_TUNNEL.md (external access)
    ↓
DOCUMENTATION_INDEX.md (nav guide)
```

---

## 🚀 Have Fun!

You now have your own Blink.new clone running locally!

- Create amazing projects
- Generate code with AI
- Execute in multiple languages
- Access from anywhere (with Cloudflare)
- Keep everything private

**Enjoy!** 🎊

---

**Questions? Check the docs or look at the code comments!**

Happy coding! 💻✨
