# Start the DiSHACLed API server
Write-Host "Starting DiSHACLed API Server..." -ForegroundColor Cyan
Write-Host "API will be available at: http://localhost:8000" -ForegroundColor Green
Write-Host "Interactive docs at: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Check if Python is installed
try {
    $null = Get-Command py -ErrorAction Stop
} catch {
    Write-Host "Error: Python is not installed!" -ForegroundColor Red
    Write-Host "Please install Python from python.org" -ForegroundColor Yellow
    exit 1
}

# Start the API server
py -m uvicorn api.main:app --reload --port 8000
