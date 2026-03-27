#!/bin/bash

echo "Cloudflare Tunnel Setup for Blink.local"
echo "========================================"
echo ""
echo "Prerequisites:"
echo "1. Create a Cloudflare account at https://dash.cloudflare.com"
echo "2. Have a domain managed by Cloudflare"
echo ""
echo "Step 1: Install cloudflared CLI"
echo "================================"
echo "Download from: https://developers.cloudflare.com/cloudflare-one/connections/connect-applications/install-and-setup/installation/"
echo "Or use: brew install cloudflared (macOS) or apt install cloudflare-warp (Linux)"
echo ""

read -p "Have you installed cloudflared? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please install cloudflared first"
    exit 1
fi

echo ""
echo "Step 2: Authenticate with Cloudflare"
echo "====================================="
echo "Running: cloudflared tunnel login"
echo "This will open your browser to authenticate."
echo ""

cloudflared tunnel login

if [ $? -ne 0 ]; then
    echo "Authentication failed!"
    exit 1
fi

echo ""
echo "Step 3: Create Tunnel"
echo "===================="
read -p "Enter a name for your tunnel (e.g., blink-local): " TUNNEL_NAME

cloudflared tunnel create $TUNNEL_NAME

if [ $? -ne 0 ]; then
    echo "Tunnel creation failed!"
    exit 1
fi

TUNNEL_ID=$(cloudflared tunnel list | grep $TUNNEL_NAME | awk '{print $1}')
echo "Tunnel created successfully!"
echo "Tunnel ID: $TUNNEL_ID"
echo ""

echo "Step 4: Configure Tunnel"
echo "======================="
echo "You need to create a configuration file at ~/.cloudflared/config.yml"
echo ""
echo "Example configuration:"
echo "====================="
cat << 'EOF'
tunnel: <TUNNEL_ID>
credentials-file: /home/user/.cloudflared/<TUNNEL_ID>.json

ingress:
  - hostname: blink.yourdomain.com
    service: http://localhost
  - service: http_status:404
EOF

echo ""
echo "After creating the config file, run:"
echo "cloudflared tunnel route dns $TUNNEL_NAME blink.yourdomain.com"
echo ""
echo "Then start the tunnel with:"
echo "cloudflared tunnel run $TUNNEL_NAME"
echo ""

echo "Step 5: Get Tunnel Token"
echo "======================="
echo "To run the tunnel in Docker, get your token:"
cloudflared tunnel token $TUNNEL_NAME

echo ""
echo "Copy this token and set it as CLOUDFLARE_TUNNEL_TOKEN in your .env file"
echo "Then run: docker-compose up -d"
echo ""
