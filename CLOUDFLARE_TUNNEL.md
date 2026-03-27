# Cloudflare Tunnel Setup - Blink.local

Expose your local IDE to the internet safely without port forwarding.

## What You'll Get

```
Your Laptop                    Cloudflare                    Your Domain
┌─────────────────┐           ┌──────────┐                ┌──────────────┐
│ Blink.local     │ ──HTTP──> │  Tunnel  │ ───HTTPS──> │ Your Browser │
│ http://localhost│           │          │                │  Anywhere    │
└─────────────────┘           └──────────┘                └──────────────┘
```

No port forwarding. No firewall changes. Just a secure tunnel to your laptop.

---

## Prerequisites

### 1. Domain (Free Option Available)

You need a domain managed by Cloudflare. Options:

**Option A: Use existing domain**
- Already have a domain?
- Change nameservers to Cloudflare at your registrar
- Takes 5-10 minutes

**Option B: Free domain**
- Get free `.eu.org`, `.tk`, or similar
- Point nameservers to Cloudflare
- Or buy cheap `.xyz` domain ($0.99/year)

### 2. Cloudflare Account

```bash
# 1. Visit https://dash.cloudflare.com/sign-up
# 2. Create account (free tier is fine)
# 3. Add your domain
# 4. Follow instructions to change nameservers
```

---

## Installation

### Step 1: Install Cloudflared CLI

#### macOS
```bash
brew install cloudflare-warp
brew install cloudflared
```

#### Linux (Ubuntu/Debian)
```bash
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb
```

#### Windows
```bash
# Download from: https://developers.cloudflare.com/cloudflare-one/connections/connect-applications/install-and-setup/installation/

# Or with chocolatey:
choco install cloudflare-warp
choco install cloudflared
```

#### Verify Installation
```bash
cloudflared --version
# Should print version number
```

---

## Setup Tunnel

### Step 2: Authenticate

```bash
cloudflared tunnel login
```

This will:
1. Open browser to Cloudflare dashboard
2. Show list of your domains
3. Select your domain
4. You'll get authorized automatically

### Step 3: Create Tunnel

```bash
cloudflared tunnel create blink
```

This creates a tunnel named "blink". Output:
```
Tunnel credentials written to ~/.cloudflared/YOUR_TUNNEL_ID.json
Cloudflare's free tunnel ingress service (available on Alpha)
```

**Save this tunnel ID!**

### Step 4: Get Tunnel Token (for Docker)

```bash
cloudflared tunnel token blink
```

Output:
```
eyJhIjoiMTIzNDU2Nzg5MCIsInQiOiI4NzY1NDMyMTAiLCJzIjoiYXBwLmNsb3VkZmxhcmUuY29tIn0
```

Copy this entire string!

---

## Configure Tunnel

### Option A: Manual Configuration (Recommended First Time)

Create `~/.cloudflared/config.yml`:

```yaml
tunnel: blink
credentials-file: /home/youruser/.cloudflared/YOUR_TUNNEL_ID.json

ingress:
  - hostname: blink.yourdomain.com
    service: http://localhost:80
  - service: http_status:404
```

Replace:
- `blink` with your tunnel name
- `YOUR_TUNNEL_ID` with actual ID
- `yourdomain.com` with your domain
- `localhost` if Blink isn't on localhost

### Option B: Run Tunnel Directly

```bash
cloudflared tunnel run blink
```

This will start the tunnel with default settings.

---

## Add DNS Record

Point your domain to Cloudflare tunnel:

```bash
cloudflared tunnel route dns blink blink.yourdomain.com
```

This creates DNS record automatically:
- `blink.yourdomain.com` → Cloudflare Tunnel → Your laptop

---

## Test Tunnel Locally

```bash
# Start tunnel
cloudflared tunnel run blink

# In another terminal, test it
curl https://blink.yourdomain.com

# Or open in browser
# https://blink.yourdomain.com
```

You should see your IDE!

---

## Run Tunnel in Docker

### Step 1: Update .env

```bash
# Get your tunnel token (from Step 4 above)
CLOUDFLARE_TUNNEL_TOKEN=eyJhIjoiMTIzNDU2Nzg5MCIsInQiOiI4NzY1NDMyMTAiLCJzIjoiYXBwLmNsb3VkZmxhcmUuY29tIn0
```

### Step 2: Restart Blink

```bash
docker-compose restart cloudflare-tunnel

# Check status
docker-compose logs cloudflare-tunnel
```

### Step 3: Access Remotely

```
https://blink.yourdomain.com
```

---

## Troubleshooting

### Tunnel Not Connecting

```bash
# Check tunnel status
cloudflared tunnel status blink

# View logs
cloudflared tunnel run blink

# Check firewall isn't blocking
sudo ufw allow out to any port 443
```

### DNS Not Resolving

```bash
# Check DNS is pointing to Cloudflare
dig blink.yourdomain.com

# Should show Cloudflare IP addresses
# If not, wait 24 hours for propagation or check nameserver settings
```

### Certificate Errors

```bash
# Cloudflare provides free SSL automatically
# If you see cert errors:
# 1. Wait 5-10 minutes for propagation
# 2. Clear browser cache (Ctrl+Shift+Del)
# 3. Try incognito window
```

### CORS Errors

The `docker-compose.yml` and `nginx.conf` already handle CORS.

If still issues:
```python
# Edit backend/project/settings.py
CORS_ALLOWED_ORIGINS = [
    'https://blink.yourdomain.com',  # Add your domain
    'http://localhost',
]
```

---

## Security

### Cloudflare Tunnel Security

✓ **No Port Forwarding** - No firewall holes
✓ **TLS Encrypted** - All traffic encrypted
✓ **DDoS Protection** - Cloudflare protects you
✓ **Automatic Certificates** - Free HTTPS
✓ **Restricted Tunnels** - Only your domain can access

### Best Practices

1. **Keep token secret**
   ```bash
   # Never commit CLOUDFLARE_TUNNEL_TOKEN to git
   # Keep in .env (already in .gitignore)
   ```

2. **Change Django secret**
   ```bash
   # Edit .env
   DJANGO_SECRET_KEY=your-new-long-random-string
   ```

3. **Use strong Code-Server password**
   ```bash
   CODE_SERVER_PASSWORD=VeryLongSecurePassword123!@#
   ```

4. **Monitor access logs**
   - Visit Cloudflare dashboard
   - Analytics > Traffic
   - View who accessed your tunnel

---

## Advanced Configuration

### Multiple Domains

```yaml
# ~/.cloudflared/config.yml
tunnel: blink
credentials-file: /home/user/.cloudflared/TUNNEL_ID.json

ingress:
  - hostname: blink.yourdomain.com
    service: http://localhost:80
  - hostname: code.yourdomain.com
    service: http://localhost:8443
  - hostname: api.yourdomain.com
    service: http://localhost:8000
  - service: http_status:404
```

Then create DNS records:
```bash
cloudflared tunnel route dns blink blink.yourdomain.com
cloudflared tunnel route dns blink code.yourdomain.com
cloudflared tunnel route dns blink api.yourdomain.com
```

### Custom Port

If Blink runs on different port:

```yaml
ingress:
  - hostname: blink.yourdomain.com
    service: http://localhost:3000  # Change port here
  - service: http_status:404
```

### HTTPS Only

```yaml
ingress:
  - hostname: blink.yourdomain.com
    service: http://localhost:80
    originRequest:
      httpHostHeader: localhost
  - service: http_status:404
```

---

## Systemd Service (Linux)

Run tunnel automatically on boot:

Create `/etc/systemd/system/cloudflared.service`:

```ini
[Unit]
Description=Cloudflare Tunnel
After=network.target

[Service]
Type=simple
User=youruser
ExecStart=/usr/local/bin/cloudflared tunnel run blink
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable it:
```bash
sudo systemctl daemon-reload
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

Check status:
```bash
sudo systemctl status cloudflared
sudo journalctl -u cloudflared -f
```

---

## Docker-Only Setup (No Local CLI)

If you only want Docker tunnel (no local CLI):

Docker handles tunnel automatically. Just:

1. Get token: `cloudflared tunnel token blink` (run locally once)
2. Update .env with token
3. Start Docker: `docker-compose up -d`
4. Access: `https://blink.yourdomain.com`

Done!

---

## Monitoring

### View Live Requests

```bash
# Local tunnel
cloudflared tunnel run blink

# Watch for requests
```

### Cloudflare Dashboard

1. Visit https://dash.cloudflare.com
2. Select domain
3. Analytics → Traffic
4. See real-time access logs

### Docker Logs

```bash
docker-compose logs cloudflare-tunnel -f
```

---

## Stopping Tunnel

### Graceful Shutdown

```bash
# If running in terminal
Ctrl+C

# If running in Docker
docker-compose stop cloudflare-tunnel

# Restart
docker-compose start cloudflare-tunnel
```

### Delete Tunnel

If you no longer need it:

```bash
# Stop tunnel first
docker-compose stop cloudflare-tunnel

# Delete tunnel
cloudflared tunnel delete blink

# Remove DNS record (optional)
# Do this in Cloudflare dashboard manually
```

---

## Cost

**Everything is Free!**

- Cloudflare Tunnel: FREE
- Domain (if using free registrar): FREE
- SSL Certificate: FREE
- Bandwidth: FREE (fair use)

Only paid if you:
- Buy premium domain
- Add Cloudflare paid features

---

## Pro Tips

### 1. Test Before Going Live

```bash
# Test locally first
curl https://blink.yourdomain.com

# Make sure it works
```

### 2. Monitor Bandwidth

Cloudflare shows usage in dashboard. If suspicious:
- Check Docker logs
- Look at access logs in Cloudflare
- Might be bots crawling

### 3. Custom Branding

Add custom error pages in Cloudflare dashboard:
- Rules → Custom Error Pages
- Make errors match your style

### 4. Performance

Cloudflare auto-caches static content:
- Faster load times
- Reduced bandwidth
- Automatic optimization

---

## Next Steps

1. **Setup domain** (if you don't have one)
2. **Add to Cloudflare** (update nameservers)
3. **Create tunnel** (`cloudflared tunnel create blink`)
4. **Get token** (`cloudflared tunnel token blink`)
5. **Update .env** with token
6. **Restart Docker** (`docker-compose restart`)
7. **Visit domain** (https://blink.yourdomain.com)

---

## Support

### Official Docs
- https://developers.cloudflare.com/cloudflare-one/connections/connect-applications/

### Troubleshooting
- https://developers.cloudflare.com/cloudflare-one/troubleshooting/

### Community
- Cloudflare Forum: https://community.cloudflare.com/
- GitHub Issues: Check project repo

---

## Summary

```bash
# 1. Install cloudflared
brew install cloudflared  # macOS
# apt install cloudflared  # Linux

# 2. Authenticate
cloudflared tunnel login

# 3. Create tunnel
cloudflared tunnel create blink

# 4. Get token
cloudflared tunnel token blink
# Copy output to .env

# 5. Setup DNS
cloudflared tunnel route dns blink blink.yourdomain.com

# 6. Restart Docker
docker-compose restart cloudflare-tunnel

# 7. Access
https://blink.yourdomain.com
```

That's it! Your IDE is now accessible from anywhere.

Happy coding from anywhere! 🚀
