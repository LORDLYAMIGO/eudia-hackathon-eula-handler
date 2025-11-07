# EULA Handler API - Start Script
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Starting EULA Handler API Server" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Change to the api directory
Set-Location -Path "api"

Write-Host "Starting server on http://localhost:8000" -ForegroundColor Green
Write-Host ""
Write-Host "Available endpoints:" -ForegroundColor Yellow
Write-Host "  - http://localhost:8000/docs (Swagger UI)" -ForegroundColor White
Write-Host "  - http://localhost:8000/redoc (ReDoc)" -ForegroundColor White
Write-Host "  - http://localhost:8000/eula/latest?domain=chatgpt.com" -ForegroundColor White
Write-Host "  - http://localhost:8000/eula/archive?domain=chatgpt.com" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Red
Write-Host ""

# Start the server
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
