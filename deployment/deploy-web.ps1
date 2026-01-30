#!/usr/bin/env pwsh
# Build and deploy React web interface

param(
    [string]$Hostname = "pi5.local",
    [string]$User = "fadi"
)

$PI_HOST = $Hostname
$PI_USER = $User
$PI_DIR = "/home/fadi/pi-tanky"

Write-Host "Building React Web Interface..." -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Check if Node.js is installed
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: npm not found. Please install Node.js first." -ForegroundColor Red
    Write-Host "Download from: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Install dependencies if needed
if (-not (Test-Path "web/node_modules")) {
    Write-Host "Installing React dependencies..." -ForegroundColor Green
    Push-Location web
    npm install
    Pop-Location
}

# Build React app
Write-Host "Building React app for production..." -ForegroundColor Green
Push-Location web
npm run build
Pop-Location

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: React build failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Deploying to Raspberry Pi..." -ForegroundColor Cyan

# Create remote directory
Write-Host "Creating directories..." -ForegroundColor Green
ssh "$PI_USER@$PI_HOST" "mkdir -p $PI_DIR/web/build"

# Deploy web server Python script
Write-Host "Copying web_server.py..." -ForegroundColor Green
scp web_server.py "$PI_USER@$PI_HOST`:$PI_DIR/"

# Deploy requirements.txt
Write-Host "Copying requirements.txt..." -ForegroundColor Green
scp requirements.txt "$PI_USER@$PI_HOST`:$PI_DIR/"

# Deploy React build
Write-Host "Copying React build files..." -ForegroundColor Green
scp -r web/build/* "$PI_USER@$PI_HOST`:$PI_DIR/web/build/"

# Install Python dependencies on Pi
Write-Host "Installing Python dependencies on Pi..." -ForegroundColor Green
ssh "$PI_USER@$PI_HOST" "pip3 install -r $PI_DIR/requirements.txt --user"

# Create and set permissions for log file
Write-Host "Setting up log file..." -ForegroundColor Green
ssh "$PI_USER@$PI_HOST" "touch $PI_DIR/tanky.log && chmod 664 $PI_DIR/tanky.log"

# Make web_server.py executable
Write-Host "Setting permissions..." -ForegroundColor Green
ssh "$PI_USER@$PI_HOST" "chmod +x $PI_DIR/web_server.py"

# Deploy systemd service file
Write-Host "Setting up systemd service for auto-start..." -ForegroundColor Green
scp deployment/pi-tanky-web.service "$PI_USER@$PI_HOST`:~/"
ssh "$PI_USER@$PI_HOST" "sudo mv ~/pi-tanky-web.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable pi-tanky-web.service"
Write-Host "Service enabled - will start on boot" -ForegroundColor Green

# Start the service
Write-Host "Starting web server..." -ForegroundColor Green
ssh "$PI_USER@$PI_HOST" "sudo systemctl restart pi-tanky-web.service"

# Wait a moment and check status
Start-Sleep -Seconds 2
$status = ssh "$PI_USER@$PI_HOST" "sudo systemctl is-active pi-tanky-web.service"

Write-Host ""
if ($status -match "active") {
    Write-Host "Deployment successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Web server is running!" -ForegroundColor Green
    Write-Host "Access at: http://pi5.local:5000" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Yellow
    Write-Host "  tanky web status   - Check server status" -ForegroundColor White
    Write-Host "  tanky web restart  - Restart server" -ForegroundColor White
    Write-Host "  tanky web stop     - Stop server" -ForegroundColor White
    Write-Host "  tanky logs         - View logs" -ForegroundColor White
} else {
    Write-Host "Deployment completed but service may not be running" -ForegroundColor Yellow
    Write-Host "Check logs with: tanky logs" -ForegroundColor Yellow
}
