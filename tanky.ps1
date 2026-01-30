#!/usr/bin/env pwsh
# Pi-Tanky Command Line Tool

param(
    [Parameter(Position=0)]
    [string]$Command,
    
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Args
)

$ScriptRoot = $PSScriptRoot

function Show-Help {
    Write-Host "Pi-Tanky Command Line Tool" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\tanky.ps1 <command>" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Green
    Write-Host "  deploy        Deploy everything (Python + web interface)"
    Write-Host "  run           Run motor_control.py on Raspberry Pi"
    Write-Host "  interactive   Real-time keyboard control (w/s/a/d)"
    Write-Host "  web start     Start web server on Raspberry Pi"
    Write-Host "  web stop      Stop web server on Raspberry Pi"
    Write-Host "  web restart   Restart web server on Raspberry Pi"
    Write-Host "  web status    Check web server status"
    Write-Host "  monitor       Run and stream live output to VS Code"
    Write-Host "  logs          Stream logs from Raspberry Pi"
    Write-Host "  ssh           SSH into Raspberry Pi"
    Write-Host "  help          Show this help message"
    Write-Host ""
}

function Invoke-Deploy {
    Write-Host "Deploying everything to Raspberry Pi..." -ForegroundColor Cyan
    Write-Host ""
    
    # Deploy Python code
    Write-Host "[1/2] Deploying Python code..." -ForegroundColor Yellow
    & "$ScriptRoot/deployment/deploy.ps1" @Args
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        # Deploy web interface
        Write-Host "[2/2] Deploying web interface..." -ForegroundColor Yellow
        & "$ScriptRoot/deployment/deploy-web.ps1" @Args
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✓ Full deployment complete!" -ForegroundColor Green
            Write-Host "Access web interface at: http://pi5.local:5000" -ForegroundColor Cyan
        }
    } else {
        Write-Host ""
        Write-Host "✗ Python deployment failed, skipping web deployment" -ForegroundColor Red
        exit 1
    }
}

function Invoke-DeployWeb {
    Write-Host "Deploying web interface..." -ForegroundColor Cyan
    & "$ScriptRoot/deployment/deploy-web.ps1" @Args
}

function Invoke-Run {
    Write-Host "Running motor_control.py on Raspberry Pi..." -ForegroundColor Cyan
    ssh fadi@pi5.local 'cd /home/fadi/pi-tanky && sudo python3 motor_control.py'
}

function Invoke-SSH {
    Write-Host "Connecting to Raspberry Pi..." -ForegroundColor Cyan
    ssh fadi@pi5.local
}

function Invoke-Monitor {
    Write-Host "Running motor_control.py with live output..." -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
    Write-Host "" 
    ssh -t fadi@pi5.local 'cd /home/fadi/pi-tanky && sudo python3 -u motor_control.py 2>&1'
}

function Invoke-Interactive {
    Write-Host "Starting interactive control mode..." -ForegroundColor Cyan
    Write-Host "Controls: w/s (forward/back), a/d (turn), =/- or arrows (speed), SPACE (stop), q (quit)" -ForegroundColor Yellow
    Write-Host ""
    ssh -t fadi@pi5.local 'cd /home/fadi/pi-tanky && sudo python3 -u motor_control.py --interactive'
}

function Invoke-Logs {
    Write-Host "Streaming logs from Raspberry Pi..." -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
    Write-Host ""
    
    $logFile = if ($Args.Count -gt 0) { $Args[0] } else { "/home/fadi/pi-tanky/tanky.log" }
    
    # Check if log file exists, if not tail system logs
    ssh -t fadi@pi5.local "if [ -f $logFile ]; then tail -f $logFile; else echo 'Log file not found. Showing system logs...'; sudo journalctl -f -u pi-tanky 2>/dev/null || tail -f /var/log/syslog | grep -i tanky; fi"
}

function Invoke-Web {
    $action = if ($Args.Count -gt 0) { $Args[0] } else { "" }
    
    switch ($action.ToLower()) {
        "start" {
            Write-Host "Starting web server on Raspberry Pi..." -ForegroundColor Cyan
            ssh fadi@pi5.local "sudo systemctl start pi-tanky-web.service"
            Write-Host "Web server started" -ForegroundColor Green
            Write-Host "Access at: http://pi5.local:5000" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "To view logs:" -ForegroundColor Cyan
            Write-Host "  tanky logs" -ForegroundColor White
        }
        "stop" {
            Write-Host "Stopping web server..." -ForegroundColor Cyan
            ssh fadi@pi5.local "sudo systemctl stop pi-tanky-web.service"
            Write-Host "Web server stopped" -ForegroundColor Green
        }
        "restart" {
            Write-Host "Restarting web server..." -ForegroundColor Cyan
            ssh fadi@pi5.local "sudo systemctl restart pi-tanky-web.service"
            Write-Host "Web server restarted" -ForegroundColor Green
            Write-Host "Access at: http://pi5.local:5000" -ForegroundColor Yellow
        }
        "status" {
            Write-Host "Checking web server status..." -ForegroundColor Cyan
            ssh fadi@pi5.local "sudo systemctl status pi-tanky-web.service"
        }
        default {
            Write-Host "Usage: tanky web [start|stop|restart|status]" -ForegroundColor Yellow
        }
    }
}

# Main command dispatcher
switch ($Command.ToLower()) {
    "deploy" { Invoke-Deploy }
    "deploy-web" { Invoke-DeployWeb }
    "run" { Invoke-Run }
    "interactive" { Invoke-Interactive }
    "monitor" { Invoke-Monitor }
    "logs" { Invoke-Logs }
    "web" { Invoke-Web }
    "ssh" { Invoke-SSH }
    "help" { Show-Help }
    default {
        if ([string]::IsNullOrWhiteSpace($Command)) {
            Show-Help
        } else {
            Write-Host "Unknown command: $Command" -ForegroundColor Red
            Write-Host ""
            Show-Help
        }
    }
}
