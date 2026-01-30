# Pi-Tanky Fresh Install Guide

This guide will help you set up Pi-Tanky on a fresh Raspberry Pi.

## Prerequisites

### On Your Raspberry Pi:
- Raspberry Pi 5 with Raspberry Pi OS installed
- Network connection (WiFi or Ethernet)
- SSH enabled
- Hostname set to `pi5` (or update scripts with your hostname)
- User: `fadi`

### On Your Windows PC:
- Node.js and npm installed (for building React app)
- PowerShell
- SSH client (included in Windows 10/11)

## Quick Start Installation

### 1. Set up SSH Key Authentication (One-time setup)

```powershell
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -f $HOME/.ssh/id_ed25519 -N '""'

# Copy key to your Pi (enter your password when prompted)
type $HOME\.ssh\id_ed25519.pub | ssh fadi@pi5.local "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### 2. Clone the Repository

```powershell
cd C:\Users\fadis\source\repos
git clone <your-repo-url> pi-tanky
cd pi-tanky
```

### 3. Set up PowerShell Function

```powershell
# Add tanky function to your PowerShell profile
$profilePath = $PROFILE
if (-not (Test-Path $profilePath)) { 
    New-Item -ItemType File -Path $profilePath -Force | Out-Null 
}
Add-Content $profilePath "`nfunction tanky { & 'c:\Users\fadis\source\repos\pi-tanky\tanky.ps1' @args }"

# Reload profile
. $PROFILE
```

### 4. Deploy Motor Control

```powershell
# Deploy motor control script
tanky deploy
```

This will:
- Create `/home/fadi/pi-tanky` directory on the Pi
- Deploy `motor_control.py`
- Set up log file with proper permissions
- Make scripts executable

### 5. Deploy Web Interface

```powershell
# Build and deploy web interface (first time)
tanky deploy-web
```

This will:
- Install React dependencies locally
- Build the React app
- Deploy all web files to the Pi
- Install Python dependencies (Flask, SocketIO, etc.)
- Set up systemd service for auto-start
- Start the web server

**Note:** First build may take a few minutes to install npm packages.

### 6. Access the Web Interface

Open your browser and go to:
```
http://pi5.local:5000
```

The web interface will:
- ✅ Start automatically when Pi boots
- ✅ Restart automatically if it crashes
- ✅ Work on desktop and mobile devices

## Usage

### Control Commands

```powershell
# Deploy updates to motor control
tanky deploy

# Rebuild and deploy web interface
tanky deploy-web

# Run motor test (automatic test sequence)
tanky run

# Interactive control (keyboard: WASD)
tanky interactive

# Web server management
tanky web status    # Check if server is running
tanky web start     # Start server
tanky web stop      # Stop server
tanky web restart   # Restart server

# View logs
tanky logs          # Stream live logs
tanky monitor       # Run motor script with live output

# SSH into Pi
tanky ssh
```

## Testing the Setup

### Test 1: Motor Control Script

```powershell
tanky run
```

You should see:
- Motor controller initialized
- Motors moving at 30%, 50%, 75%, 100%
- Motors should physically move (if connected)

### Test 2: Interactive Control

```powershell
tanky interactive
```

Use keyboard:
- W/S: Forward/Backward
- A/D: Turn Left/Right
- +/-: Increase/Decrease speed
- SPACE: Stop
- Q: Quit

### Test 3: Web Interface

1. Open http://pi5.local:5000 in browser
2. You should see the Pi-Tanky control interface
3. Click/tap buttons to control
4. Use keyboard (same as interactive mode)

## Troubleshooting

### Pi is not reachable

```powershell
# Test connection
ping pi5.local

# If that fails, find Pi's IP address
# (Check your router or connect monitor to Pi and run: hostname -I)
# Then use IP instead:
.\tanky.ps1 deploy -Hostname 192.168.1.XXX
```

### Web server not starting

```powershell
# Check service status
tanky web status

# View logs
tanky logs

# Common fixes:
ssh fadi@pi5.local "pip3 install -r /home/fadi/pi-tanky/requirements.txt --user"
tanky web restart
```

### Motors not moving

1. Check GPIO pins are correct in motor_control.py
2. Ensure motor driver is properly connected
3. Check power supply to motors
4. Review logs: `tanky logs`

### Permission errors

```powershell
# Fix log file permissions
ssh fadi@pi5.local "chmod 664 /home/fadi/pi-tanky/tanky.log"
```

## File Structure

```
pi-tanky/
├── motor_control.py           # Motor control library
├── web_server.py              # Flask WebSocket server
├── requirements.txt           # Python dependencies
├── tanky.ps1                  # Main CLI tool
├── deployment/
│   ├── deploy.ps1            # Motor control deployment
│   ├── deploy-web.ps1        # Web interface deployment
│   └── pi-tanky-web.service  # Systemd service file
└── web/
    ├── package.json          # React dependencies
    ├── public/
    └── src/
        ├── App.js            # Main React component
        └── App.css           # Styles
```

## Next Steps

- Set up camera streaming (Phase 3 in PRD)
- Add autonomous navigation features
- Implement additional sensors

## Support

Check logs for errors:
```powershell
tanky logs
```

Or SSH into the Pi for debugging:
```powershell
tanky ssh
```
