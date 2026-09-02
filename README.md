# DiSHACLed - Water Level Monitoring Demo

A demonstration system for semantic water level monitoring with JSON-LD, SHACL shapes, and real-time data streams.

## Overview

This project simulates water level monitoring from multiple sources with different units:
- **Source A**: Publishes measurements in centimeters (1300-2200 cm)
- **Source B**: Publishes measurements in millimeters (13000-22000 mm)
- **Antwerp**: Proxy endpoint using the currently selected primary source

The system includes:
- Mocked JSON-LD API endpoints for real-time measurements
- Synchronized data sources (Source A and B always show same measurement, different units)
- Automatic value updates every 5 seconds with ±2% realistic variation
- Web-based control center with slider and primary source selector
- Water level thresholds table with 5 warning levels
- SHACL shapes and ODRL policies for semantic data validation
- Standard semantic vocabularies (SOSA, Dublin Core Terms, Schema.org)
- Metadata descriptions with WGS84 coordinates

## Live Deployment

The DiSHACLed application is deployed on Azure:
- **Frontend**: https://dishacled-frontend.azurewebsites.net
- **API**: https://dishacled-api.azurewebsites.net
- **API Documentation**: https://dishacled-api.azurewebsites.net/docs

📘 **[Complete Azure Deployment Guide](AZURE_DEPLOYMENT.md)** - Detailed deployment documentation, architecture, and troubleshooting

## Project Structure

```
DiSHACLed/
├── api/                    # FastAPI backend
│   ├── main.py            # Main API application
│   ├── models.py          # Pydantic data models
│   └── routers/           # API route handlers
│       ├── sources.py     # Water source endpoints
│       ├── control.py     # Control endpoints
│       └── metadata.py    # SHACL/ODRL/metadata
├── frontend/              # Web interface
│   ├── index.html        # Control center UI
│   ├── app.py            # Flask server for Azure deployment
│   ├── requirements.txt  # Frontend Python dependencies
│   ├── css/              # Styles
│   └── js/               # Client-side logic
├── requirements.txt       # API Python dependencies
├── start.ps1              # Start everything (Windows)
└── README.md              # This file
```

## Getting Started

### Prerequisites
- Python 3.11+
- pip

### Local Development

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the API server:
```bash
uvicorn api.main:app --reload --port 8000
```

3. Open the frontend:
   - Open `frontend/index.html` in your browser
   - Or serve it using Python: `python -m http.server 3000 -d frontend`

### Azure Deployment

The application is deployed to Azure App Service. To deploy updates:

**Deploy API:**
```bash
az webapp up --resource-group dishacled-rg --name dishacled-api --runtime "PYTHON:3.11" --sku B1 --location westeurope
```

**Deploy Frontend:**
```bash
cd frontend
az webapp up --resource-group dishacled-rg --name dishacled-frontend --runtime "PYTHON:3.11" --sku B1 --location westeurope
cd ..
```

### Usage

1. Access the API Control Center at `http://localhost:3000`
2. Use the slider to adjust water levels (0-100%)
3. Select primary source with radio buttons (Source A or Source B)
4. View real-time data with automatic 5-second refresh
5. Check water level thresholds table for warning levels
6. Observe synchronized measurements (Source B = Source A × 10)

## API Endpoints

### Water Sources (v1 – schema.org `PropertyValue`)
- `GET /api/v1/source-a/current` - Source A water level (1300-2200 cm)
- `GET /api/v1/source-b/current` - Source B water level (13000-22000 mm)
- `GET /api/v1/antwerp/current` - Antwerp proxy (uses active source)

### Water Sources (v2 – SOSA/QUDT `Observation`)
- `GET /api/v2/source-a/current` - Source A as `sosa:Observation` → `qudt:QuantityValue` (unit `unit:CentiM`)
- `GET /api/v2/source-b/current` - Source B as `sosa:Observation` → `qudt:QuantityValue` (unit `unit:MilliM`)
- `GET /api/v2/antwerp/current` - Antwerp proxy (uses active source)

Both API versions share the same water-level slider and active-source toggle, so
they always stay synchronized. Measurement responses are served as
`application/ld+json` by default (content-negotiable: a client requesting only
`application/json` still receives that content type).

**Additional measurement fields**
- `SensorBrand` – present on every measurement: `HydroMeasureX5` (Source A) / `WaterProber3` (Source B). In v2 it is nested under `sosa:madeBySensor`.
- `waterTemperature` – Source B only, always `18°C` (also surfaced on the Antwerp endpoint when Source B is the active source).

### Control
- `POST /api/v1/control/set-level` - Set water level percentage
- `POST /api/v1/control/set-active-source` - Set primary source
- `GET /api/v1/control/active-source` - Get current active source

### Metadata
- `GET /api/v1/shapes/shacl` - SHACL validation shapes
- `GET /api/v1/shapes/odrl` - ODRL usage policies
- `GET /api/v1/catalog` - DCAT-AP data catalog
- `GET /api/v1/metadata` - Service and dataset metadata (legacy)
- `GET /docs` - Interactive API documentation

## Technologies

- **Backend**: Python 3.11, FastAPI, Pydantic, Uvicorn, Gunicorn
- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Flask (for Azure deployment)
- **Hosting**: Azure App Service (Linux, Python 3.11)
- **Semantic Web**: JSON-LD, SHACL, ODRL, SOSA/SSN, Dublin Core
- **Standards**: W3C (Schema.org, SOSA), ISO TC 211, INSPIRE

## Technical Details

### Data Synchronization
The application ensures Source A and Source B always return synchronized measurements:
- **Shared Cache**: Both sources use `_base_level_cache` with timestamp-based recalculation
- **5-Second Windows**: Values recalculate every 5 seconds with ±2% realistic variation
- **Race-Condition Protection**: Timestamp updates before value calculation prevent concurrent recalculations
- **Perfect 10:1 Ratio**: Source B (mm) = Source A (cm) × 10, guaranteed synchronized
- **Single Worker**: Gunicorn runs with 1 worker to maintain consistent shared state

### Auto-Update Mechanism
- **Backend**: Recalculates base water level every 5 seconds
- **Frontend**: Auto-refresh fetches new data every 5 seconds
- **Cache-Busting**: All fetch requests include `cache: 'no-store'` headers to prevent browser caching
- **Smooth Updates**: Values stay consistent within 5-second windows, then smoothly transition

### Why Single Worker?
Multiple Gunicorn workers would each maintain separate in-memory state, causing:
- Random value jumps as requests hit different workers
- Desynchronization between Source A and Source B
- Inconsistent readings across refreshes

Single worker ensures all requests see the same cached state.

## Azure Infrastructure

- **Subscription**: DiSHACLed
- **Resource Group**: dishacled-rg (West Europe)
- **App Service Plan**: dishacled-plan (B1 Linux)
- **Web Apps**: 
  - dishacled-api (Python 3.11 with Gunicorn + Uvicorn, single worker for state consistency)
  - dishacled-frontend (Python 3.11 with Flask + Gunicorn)

## Documentation

- **[README.md](README.md)** - This file, project overview and quick start
- **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step local development and deployment guide
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Detailed project structure and features
- **[AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)** - Complete Azure deployment guide with architecture and troubleshooting
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Quick deployment checklist and commands
- **[frontend/README.md](frontend/README.md)** - Frontend-specific deployment documentation
- **[CHANGELOG.md](CHANGELOG.md)** - Project version history and changes

## License

This is a demonstration project for educational purposes.
