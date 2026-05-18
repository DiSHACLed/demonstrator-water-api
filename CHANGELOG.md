# Changelog

All notable changes to the DiSHACLed project are documented in this file.

## [1.2.0] - 2026-04-02 - Synchronization & Stability Improvements

### Fixed

#### Critical Race Condition Resolution
- **Fixed race condition** in `get_base_level()` function that caused Source A and Source B to occasionally show different measurements
  - Moved timestamp update (`_base_level_cache["last_update"] = current_time`) to FIRST line of recalculation block
  - Prevents concurrent requests from both entering the recalculation block simultaneously
  - Ensures both sources always return synchronized measurements (10:1 ratio maintained)

#### Multi-Worker State Inconsistency
- **Changed from 4 workers to 1 worker** to maintain consistent shared state
  - Previous: `gunicorn -w 4` caused random value jumps as each worker maintained separate state
  - Current: `gunicorn -w 1` ensures all requests see consistent cached values
  - Eliminated unexpected value jumps between requests

#### Browser Caching Issues
- **Added cache-busting headers** to all frontend API fetch calls
  - `cache: 'no-store'` prevents browser from caching API responses
  - `Cache-Control: 'no-cache'` ensures fresh data on every request
  - Fixes mismatches when changing sources or water levels

### Changed

#### Timing Adjustments
- **Backend recalculation interval**: Changed from per-second to every 5 seconds
  - More realistic simulation of real sensor update frequency
  - Reduces server load while maintaining demonstration value
  - Values remain stable within 5-second windows

- **Frontend auto-refresh**: Changed from 2 seconds to 5 seconds
  - Synchronized with backend recalculation timing
  - Updated UI text: "Auto-refresh data (every 5 seconds)"
  - Improved user experience with coordinated updates

- **Source switching delay**: Increased from 100ms to 300ms
  - Ensures backend state propagates before frontend refreshes
  - More reliable synchronization after source changes

- **Water level change delay**: Added 200ms delay before refresh
  - Allows backend to update cached values
  - Prevents displaying stale data after slider changes

### Technical Details

#### Synchronization Mechanism
- Source A and Source B now guaranteed to return synchronized measurements
  - Both sources use shared `_base_level_cache` with timestamp-based recalculation
  - Source B value is exactly 10× Source A value (mm = cm × 10)
  - ±2% random variation applied once per 5-second window
  - All concurrent requests within same 5-second window get identical base value

#### Azure Configuration Updates
- API startup command: `gunicorn -w 1 -k uvicorn.workers.UvicornWorker api.main:app`
- Frontend deployment includes updated cache-busting JavaScript

### Verified
- ✅ 30+ rapid synchronization tests confirm perfect 10:1 ratio maintained
- ✅ No race conditions detected across recalculation boundaries
- ✅ Values stable with only natural 5-second updates
- ✅ Source switching works reliably with Antwerp endpoint proxy
- ✅ Water level changes from 0-100% maintain synchronization

## [1.1.0] - 2026-03-30 - Azure Deployment

### Added

#### Azure Deployment Infrastructure
- Deployed to Azure App Service in DiSHACLed subscription
- Resource Group: `dishacled-rg` (West Europe)
- App Service Plan: `dishacled-plan` (B1 Linux)
- Live URLs:
  - Frontend: https://dishacled-frontend.azurewebsites.net
  - API: https://dishacled-api.azurewebsites.net
  - API Docs: https://dishacled-api.azurewebsites.net/docs

#### New Files
- `frontend/app.py` - Flask application to serve static files on Azure
- `frontend/requirements.txt` - Python dependencies for frontend deployment (Flask, Gunicorn)
- `AZURE_DEPLOYMENT.md` - Comprehensive Azure deployment guide
- `frontend/README.md` - Frontend deployment documentation
- `DEPLOYMENT_CHECKLIST.md` - Quick deployment checklist and reference
- `CHANGELOG.md` - This changelog

#### Dependencies
- Added `gunicorn==21.2.0` to root `requirements.txt` for API production server
- Created `frontend/requirements.txt` with Flask and Gunicorn for frontend

### Changed

#### Configuration Updates
- Updated `frontend/js/app.js`:
  - Changed `API_BASE_URL` from `http://localhost:8000/api/v1` to `https://dishacled-api.azurewebsites.net/api/v1`
  - Enables frontend to connect to deployed API

#### Azure Startup Commands
- **API**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.main:app`
  - Uses Gunicorn with 4 workers and Uvicorn worker class for ASGI support
- **Frontend**: `gunicorn -w 2 app:app`
  - Uses Gunicorn with 2 workers for Flask application

#### Documentation
- Updated `README.md`:
  - Added live deployment URLs
  - Updated project structure with new files
  - Added Azure infrastructure details
  - Added documentation index
  - Added Azure deployment section

- Updated `QUICKSTART.md`:
  - Added live demo section at the top
  - Added Azure deployment instructions
  - Added deployment testing commands
  - Noted Gunicorn dependency

- Updated `PROJECT_OVERVIEW.md`:
  - Added live deployment section
  - Updated project structure
  - Added three deployment options (live, local, custom Azure)
  - Updated file descriptions

- Updated `.gitignore`:
  - Added Azure deployment artifacts (`deploy-api.zip`, `deploy-frontend.zip`)
  - Added `.azure/` directory
  - Added `local.settings.json`

### Technical Details

#### API Deployment
- Runtime: Python 3.11 on Linux
- Server: Gunicorn with Uvicorn ASGI workers
- Workers: 4 (optimized for API workload)
- Dependencies: FastAPI, Uvicorn, Gunicorn, Pydantic, PyLD, python-dateutil

#### Frontend Deployment
- Runtime: Python 3.11 on Linux
- Server: Flask with Gunicorn WSGI
- Workers: 2 (optimized for static file serving)
- Dependencies: Flask, Gunicorn
- Static files: HTML, CSS, JavaScript served by Flask

#### Deployment Method
- Used `az webapp up` command for streamlined deployment
- Automatic ZIP creation and upload
- Automatic dependency installation via requirements.txt
- Preserved local development capability

### Infrastructure as Code

Resource creation commands:
```bash
# Resource Group
az group create --name dishacled-rg --location westeurope

# App Service Plan
az appservice plan create --name dishacled-plan \
  --resource-group dishacled-rg \
  --location westeurope \
  --is-linux --sku B1

# API Web App
az webapp create --name dishacled-api \
  --resource-group dishacled-rg \
  --plan dishacled-plan \
  --runtime "PYTHON:3.11"

# Frontend Web App
az webapp create --name dishacled-frontend \
  --resource-group dishacled-rg \
  --plan dishacled-plan \
  --runtime "PYTHON:3.11"
```

## [1.0.0] - Initial Release

### Features
- FastAPI backend with water level monitoring endpoints
- Two data sources (Source A in cm, Source B in mm)
- Antwerp proxy endpoint using active source
- Control API for setting water levels and active source
- SHACL shapes for data validation
- ODRL policies for usage rights
- DCAT-AP catalog in European standard format
- JSON-LD formatted responses with semantic vocabularies
- Web-based control center with visual slider
- Real-time data display with auto-refresh
- Water level thresholds table with highlighting
- Responsive design with gradient styling
- Interactive API documentation at /docs
- Local development scripts for Windows (PowerShell)

### Technologies
- Python 3.11
- FastAPI
- Uvicorn
- Pydantic
- HTML5, CSS3
- Vanilla JavaScript
- JSON-LD
- SHACL
- ODRL
- SOSA/SSN vocabularies
- Dublin Core Terms
- Schema.org

---

## Legend

- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Features that will be removed
- **Removed**: Features that were removed
- **Fixed**: Bug fixes
- **Security**: Security improvements
