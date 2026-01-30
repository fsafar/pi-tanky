# Pi-Tanky Deployment Script
# Deploys code to Raspberry Pi via SCP

param(
    [string]$Hostname = "pi5.local",
    [string]$User = "fadi"
)

$PI_HOST = $Hostname
$PI_USER = $User
$PI_DIR = "/home/fadi/pi-tanky"

Write-Host "Pi-Tanky Deployment Script" -ForegroundColor Cyan
Write-Host "=" * 40 -ForegroundColor Cyan
Write-Host "Target: $PI_USER@$PI_HOST`:$PI_DIR" -ForegroundColor Yellow
Write-Host ""

# Check if ssh is available
if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: SSH not found. Please install OpenSSH client." -ForegroundColor Red
    exit 1
}

# Create remote directory if it doesn't exist
Write-Host "Creating remote directory..." -ForegroundColor Green
ssh "$PI_USER@$PI_HOST" "mkdir -p $PI_DIR"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to connect to Raspberry Pi" -ForegroundColor Red
    Write-Host "Make sure:" -ForegroundColor Yellow
    Write-Host "  1. Raspberry Pi is powered on and connected to network" -ForegroundColor Yellow
    Write-Host "  2. You can ping pi5.local" -ForegroundColor Yellow
    Write-Host "  3. SSH is enabled on the Pi" -ForegroundColor Yellow
    exit 1
}

# Create log file with proper permissions
Write-Host "Setting up log file..." -ForegroundColor Green
ssh "$PI_USER@$PI_HOST" "touch $PI_DIR/tanky.log && chmod 664 $PI_DIR/tanky.log"

# Copy Python script
Write-Host "Copying motor_control.py..." -ForegroundColor Green
scp motor_control.py "$PI_USER@$PI_HOST`:$PI_DIR/"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to copy files" -ForegroundColor Red
    exit 1
}

# Make script executable
Write-Host "Setting permissions..." -ForegroundColor Green
ssh "$PI_USER@$PI_HOST" "chmod +x $PI_DIR/motor_control.py"

Write-Host ""
Write-Host "Deployment successful!" -ForegroundColor Green
Write-Host ""
Write-Host "To run on Raspberry Pi:" -ForegroundColor Cyan
Write-Host "  ssh $PI_USER@$PI_HOST" -ForegroundColor White
Write-Host "  cd $PI_DIR" -ForegroundColor White
Write-Host "  sudo python3 motor_control.py" -ForegroundColor White
Write-Host ""
Write-Host "Or run remotely:" -ForegroundColor Cyan
Write-Host "  ssh $PI_USER@$PI_HOST 'cd $PI_DIR && sudo python3 motor_control.py'" -ForegroundColor White
