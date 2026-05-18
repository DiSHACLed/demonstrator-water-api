# Start both API and Frontend servers
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DiSHACLed - Complete Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $null = Get-Command py -ErrorAction Stop
} catch {
    Write-Host "Error: Python is not installed!" -ForegroundColor Red
    Write-Host "Please install Python from python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Starting API server in background..." -ForegroundColor Green

# Start API in a new PowerShell window
$apiScript = @"
Write-Host 'DiSHACLed API Server' -ForegroundColor Cyan
Write-Host 'Running at: http://localhost:8000' -ForegroundColor Green
Write-Host 'Docs at: http://localhost:8000/docs' -ForegroundColor Green
Write-Host ''
py -m uvicorn api.main:app --reload --port 8000
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $apiScript

# Wait a moment for API to start
Write-Host "Waiting for API to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "Starting Frontend server in background..." -ForegroundColor Green

# Start Frontend in a new PowerShell window  
$frontendScript = @"
Write-Host 'DiSHACLed Frontend Server' -ForegroundColor Cyan
Write-Host 'Running at: http://localhost:3000' -ForegroundColor Green
Write-Host ''
py -m http.server 3000 -d frontend
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript

# Wait and show info
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  DiSHACLed is now running!" -ForegroundColor Green  
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "API Server:      http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs:        http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Control Center:  http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening Control Center in your browser..." -ForegroundColor Yellow

# Open browser
Start-Sleep -Seconds 2
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "Servers are running in separate windows." -ForegroundColor Green
Write-Host "Close those windows to stop the servers." -ForegroundColor Yellow
