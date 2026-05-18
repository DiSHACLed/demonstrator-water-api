# Start a simple HTTP server for the frontend
Write-Host "Starting DiSHACLed Frontend..." -ForegroundColor Cyan
Write-Host "Control Center will be available at: http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "Make sure the API is running at http://localhost:8000" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start Python HTTP server
py -m http.server 3000 -d frontend
