# Azure Deployment Guide

## Overview

The DiSHACLed application is deployed on Azure App Service with a Python runtime. Both the API and frontend are hosted as separate web apps within the same App Service Plan.

## Live Deployment

- **Subscription**: DiSHACLed (`<your-subscription-id>`)
- **Resource Group**: dishacled-rg
- **Location**: West Europe
- **App Service Plan**: dishacled-plan (B1 Linux)

### Deployed Applications

| Component | URL | Runtime | Entry Point |
|-----------|-----|---------|-------------|
| Frontend | https://dishacled-frontend.azurewebsites.net | Python 3.11 | Flask app with Gunicorn |
| API | https://dishacled-api.azurewebsites.net | Python 3.11 | FastAPI with Gunicorn + Uvicorn |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Azure Subscription: DiSHACLed                          │
│  └─ Resource Group: dishacled-rg (West Europe)          │
│                                                          │
│     ┌───────────────────────────────────────────┐       │
│     │  App Service Plan: dishacled-plan         │       │
│     │  SKU: B1 (Basic)                          │       │
│     │  OS: Linux                                │       │
│     │                                            │       │
│     │  ┌─────────────────────────────────────┐  │       │
│     │  │  dishacled-api                      │  │       │
│     │  │  Runtime: Python 3.11               │  │       │
│     │  │  Startup: gunicorn -w 1 -k          │  │       │
│     │  │    uvicorn.workers.UvicornWorker    │  │       │
│     │  │    api.main:app                     │  │       │
│     │  └─────────────────────────────────────┘  │       │
│     │                                            │       │
│     │  ┌─────────────────────────────────────┐  │       │
│     │  │  dishacled-frontend                 │  │       │
│     │  │  Runtime: Python 3.11               │  │       │
│     │  │  Startup: gunicorn -w 2 app:app     │  │       │
│     │  └─────────────────────────────────────┘  │       │
│     └───────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────┘
```

## Deployment Files

### API (Root Directory)

**requirements.txt**
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
gunicorn==21.2.0
pydantic==2.5.3
python-multipart==0.0.6
pyld==2.0.3
python-dateutil==2.8.2
```

**Startup Command**: `gunicorn -w 1 -k uvicorn.workers.UvicornWorker api.main:app`

**Note**: Single worker (`-w 1`) is required to maintain consistent shared state for synchronized water level readings. Multiple workers would cause random value jumps as each worker maintains separate cached state.

### Frontend (frontend/ Directory)

**requirements.txt**
```
flask==3.0.0
gunicorn==21.2.0
```

**app.py** - Flask server to serve static files:
```python
from flask import Flask, send_from_directory, send_file
import os

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
```

**Startup Command**: `gunicorn -w 2 app:app`

**js/app.js Configuration**:
```javascript
const API_BASE_URL = 'https://dishacled-api.azurewebsites.net/api/v1';
```

## Deployment Instructions

### Prerequisites

1. Azure CLI installed and configured
2. Authenticated to the DiSHACLed subscription

```powershell
# Login to Azure
az login

# Set the DiSHACLed subscription
az account set --subscription <your-subscription-id>

# Verify subscription
az account show
```

### Deploy API

From the project root directory:

```powershell
az webapp up --resource-group dishacled-rg \
  --name dishacled-api \
  --runtime "PYTHON:3.11" \
  --sku B1 \
  --location westeurope
```

The deployment:
- Creates a ZIP of the current directory
- Uploads to Azure App Service
- Installs dependencies from `requirements.txt`
- Starts with the configured startup command

### Deploy Frontend

From the project root directory:

```powershell
cd frontend

az webapp up --resource-group dishacled-rg \
  --name dishacled-frontend \
  --runtime "PYTHON:3.11" \
  --sku B1 \
  --location westeurope

cd ..
```

### Update Frontend API Configuration

Before deploying the frontend, ensure `frontend/js/app.js` points to the correct API URL:

```javascript
// For Azure deployment
const API_BASE_URL = 'https://dishacled-api.azurewebsites.net/api/v1';

// For local development
// const API_BASE_URL = 'http://localhost:8000/api/v1';
```

## Monitoring & Logs

### Enable Application Logging

```powershell
# Enable logging for API
az webapp log config --resource-group dishacled-rg \
  --name dishacled-api \
  --application-logging filesystem \
  --level information

# Enable logging for Frontend
az webapp log config --resource-group dishacled-rg \
  --name dishacled-frontend \
  --application-logging filesystem \
  --level information
```

### Stream Logs

```powershell
# Stream API logs
az webapp log tail --resource-group dishacled-rg --name dishacled-api

# Stream Frontend logs
az webapp log tail --resource-group dishacled-rg --name dishacled-frontend
```

### View in Azure Portal

1. Navigate to https://portal.azure.com
2. Go to Resource Groups > dishacled-rg
3. Select the web app
4. Go to "Log stream" or "Diagnose and solve problems"

## Management Commands

### Restart Applications

```powershell
# Restart API
az webapp restart --resource-group dishacled-rg --name dishacled-api

# Restart Frontend
az webapp restart --resource-group dishacled-rg --name dishacled-frontend
```

### Check Application Status

```powershell
# Check API status
az webapp show --resource-group dishacled-rg \
  --name dishacled-api \
  --query "{state:state, defaultHostName:defaultHostName}" \
  -o table

# Check Frontend status
az webapp show --resource-group dishacled-rg \
  --name dishacled-frontend \
  --query "{state:state, defaultHostName:defaultHostName}" \
  -o table
```

### Test Deployments

```powershell
# Test API
Invoke-RestMethod -Uri "https://dishacled-api.azurewebsites.net/" -Method Get

# Test Frontend
Invoke-WebRequest -Uri "https://dishacled-frontend.azurewebsites.net/" -UseBasicParsing -Method Head
```

## Configuration Changes

### API Startup Command

The startup command is configured to use Gunicorn with a single Uvicorn worker for optimal ASGI performance and state consistency:

```bash
gunicorn -w 1 -k uvicorn.workers.UvicornWorker api.main:app
```

- `-w 1`: Single worker process (required for shared state consistency)
- `-k uvicorn.workers.UvicornWorker`: Use Uvicorn worker for ASGI
- `api.main:app`: Module and application path

**Why single worker?** The application maintains shared state in memory (water level cache, active source). Multiple workers would each maintain separate state, causing random value jumps as requests hit different workers.

To change:
```powershell
az webapp config set --resource-group dishacled-rg \
  --name dishacled-api \
  --startup-file "gunicorn -w 1 -k uvicorn.workers.UvicornWorker api.main:app"
```

### Frontend Startup Command

```bash
gunicorn -w 2 app:app
```

- `-w 2`: 2 worker processes (lighter workload than API)
- `app:app`: Flask application

To change:
```powershell
az webapp config set --resource-group dishacled-rg \
  --name dishacled-frontend \
  --startup-file "gunicorn -w 2 app:app"
```

## Cost Optimization

Current setup uses **B1 (Basic)** tier:
- **Cost**: ~€12.41/month per app (€24.82 total for 2 apps)
- **Resources**: 1 Core, 1.75 GB RAM per app
- **Features**: Custom domains, SSL, always-on

### Cost-Saving Options

1. **Use F1 (Free) tier** for testing:
   - Limited to 60 minutes/day runtime
   - No always-on
   - No custom domains
   
2. **Scale down when not in use**:
   ```powershell
   az appservice plan update --resource-group dishacled-rg \
     --name dishacled-plan \
     --sku F1
   ```

3. **Delete resources when not needed**:
   ```powershell
   az group delete --name dishacled-rg
   ```

## Troubleshooting

### Application Won't Start

1. Check logs:
   ```powershell
   az webapp log tail --resource-group dishacled-rg --name dishacled-api
   ```

2. Verify startup command is correct
3. Ensure all dependencies in `requirements.txt`
4. Check Python version compatibility

### Frontend Can't Connect to API

1. Verify API URL in `frontend/js/app.js`
2. Check CORS configuration in `api/main.py`
3. Test API directly: https://dishacled-api.azurewebsites.net/docs

### Deployment Fails

1. Ensure you're in the correct directory
2. Check Azure CLI is authenticated
3. Verify subscription is set correctly
4. Try redeploying with `--verbose` flag

## Security Considerations

### Production Recommendations

1. **Enable HTTPS Only**:
   ```powershell
   az webapp update --resource-group dishacled-rg \
     --name dishacled-api \
     --https-only true
   ```

2. **Restrict CORS** in `api/main.py`:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://dishacled-frontend.azurewebsites.net"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. **Use Managed Identity** for inter-service communication
4. **Enable Application Insights** for monitoring
5. **Set up IP restrictions** if needed

## Next Steps

1. **Custom Domain**: Configure custom domain names
2. **SSL Certificate**: Add SSL certificates for custom domains
3. **Application Insights**: Set up monitoring and analytics
4. **CI/CD**: Configure GitHub Actions or Azure DevOps pipelines
5. **Staging Slots**: Add deployment slots for testing before production
6. **Auto-scaling**: Configure auto-scaling rules for higher traffic

## Support & Resources

- Azure App Service Documentation: https://docs.microsoft.com/azure/app-service/
- Python on Azure: https://docs.microsoft.com/azure/developer/python/
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- Flask Deployment: https://flask.palletsprojects.com/en/latest/deploying/
