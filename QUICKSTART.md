# Quick Start Guide for DiSHACLed

## Live Demo

The application is already deployed and running on Azure:
- **Frontend**: https://dishacled-frontend.azurewebsites.net
- **API**: https://dishacled-api.azurewebsites.net
- **API Docs**: https://dishacled-api.azurewebsites.net/docs

No installation needed to try it out!

## Local Development - Windows Setup

### Step 1: Install Python Dependencies

Open PowerShell in the project directory and run:

```powershell
py -m pip install -r requirements.txt
```

> **Note**: Use `py` (Python launcher) instead of `python` or `pip` on Windows if those commands aren't in your PATH.
> The `requirements.txt` includes Gunicorn for production deployment on Azure.

### Step 2: Start the API Server

```powershell
py -m uvicorn api.main:app --reload --port 8000
```

Or use the provided script:
```powershell
.\start-api.ps1
```

The API will be available at:
- Main API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- OpenAPI spec: http://localhost:8000/openapi.json

### Step 3: Open the Frontend

Option A - Direct file access:
- Open `frontend\index.html` directly in your browser

Option B - Using Python HTTP server (recommended):
```powershell
py -m http.server 3000 -d frontend
```

Then open http://localhost:3000

Or use the provided script:
```powershell
.\start-frontend.ps1
```

### Step 4: Use the Control Center

1. The Control Center will load at http://localhost:3000 (or use the live version at https://dishacled-frontend.azurewebsites.net)
2. Use the slider to adjust water levels (0-100%)
3. Select a primary source with radio buttons (Source A or Source B)
4. Click "Set as Primary" to apply the source selection
5. View water level thresholds table with real-time highlighting
6. Watch real-time data from both sources update automatically

## Azure Deployment

### Prerequisites for Deployment
- Azure CLI installed
- Authenticated to Azure subscription (DiSHACLed)

### Deploy API to Azure

```powershell
az webapp up --resource-group dishacled-rg --name dishacled-api --runtime "PYTHON:3.11" --sku B1 --location westeurope
```

### Deploy Frontend to Azure

```powershell
cd frontend
az webapp up --resource-group dishacled-rg --name dishacled-frontend --runtime "PYTHON:3.11" --sku B1 --location westeurope
cd ..
```

### View Deployment Logs

```powershell
# API logs
az webapp log tail --resource-group dishacled-rg --name dishacled-api

# Frontend logs
az webapp log tail --resource-group dishacled-rg --name dishacled-frontend
```

## Testing the API Manually

### Get Source A Data (cm)
```powershell
curl http://localhost:8000/api/v1/source-a/current
```

### Get Source B Data (mm)
```powershell
curl http://localhost:8000/api/v1/source-b/current
```

### Get Antwerp Data (proxy)
```powershell
curl http://localhost:8000/api/v1/antwerp/current
```

### Set Primary Source
```powershell
$body = @{
    source_name = "source-a"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/api/v1/control/set-active-source `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

### Get Active Source
```powershell
curl http://localhost:8000/api/v1/control/active-source
```

### Set Water Level
```powershell
$body = @{
    level_percentage = 75
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/api/v1/control/set-level `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

### Get SHACL Shapes
```powershell
curl http://localhost:8000/api/v1/shapes/shacl
```

### Get ODRL Policies
```powershell
curl http://localhost:8000/api/v1/shapes/odrl
```

### Get DCAT Catalog
```powershell
curl http://localhost:8000/api/v1/catalog
```

### Get Service Metadata (Legacy)
```powershell
curl http://localhost:8000/api/v1/metadata
```

## Understanding the Data

### JSON-LD Format
All API responses use JSON-LD format with semantic annotations:

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "sosa": "http://www.w3.org/ns/sosa/",
    "dcterms": "http://purl.org/dc/terms/",
    "measuredAt": "sosa:resultTime",
    "conformsTo": "dcterms:conformsTo",
    "source": "https://schema.org/source"
  },
  "@type": "PropertyValue",
  "@id": "urn:measurement:source-a:2026-03-25T10:30:00",
  "name": "Water Level - Source A",
  "value": 1750.5,
  "unitCode": "CMT",
  "measuredAt": "2026-03-25T10:30:00Z",
  "source": "Source A",
  "location": {
    "@type": "Place",
    "name": "Antwerp Water Monitoring Station",
    "geo": {
      "@type": "GeoCoordinates",
      "latitude": 51.222278,
      "longitude": 4.396
    }
  }
}
```

### Water Level Mapping
- **Slider**: 0-100% (percentage)
- **Source A**: 1300-2200 cm (centimeters) - formula: 1300 + (percentage * 9.0)
  - Unit code: **CMT** (centimetre - UN/CEFACT Common Code)
- **Source B**: 13000-22000 mm (millimeters) - formula: 13000 + (percentage * 90.0)
  - Unit code: **MMT** (millimetre - UN/CEFACT Common Code)
- **Antwerp**: Uses the currently active source (A or B)

Note: Source B values = Source A values × 10 (since 1 cm = 10 mm)

**About Unit Codes**: The `unitCode` property uses the UN/CEFACT Common Code standard 
(UNECE Recommendation 20), which is the recommended vocabulary for Schema.org measurements.

## Demo Scenario: Water Level Thresholds

1. Start with normal conditions (30% ≈ 1570 cm)
2. View the water level thresholds table showing 5 warning levels
3. Gradually increase the slider to 50% (~1750 cm)
4. Watch the threshold highlighting change from green to yellow
5. Continue to 80% (~2020 cm) to see higher warning levels
6. Both sources show synchronized values with ±2% variation
7. Switch primary source and see Antwerp endpoint change accordingly

## Semantic Web Features

### SHACL Shapes
Visit http://localhost:8000/api/v1/shapes/shacl to see validation rules:
- Data type constraints (xsd:decimal for coordinates and values)
- Value ranges for each source (Source A: 1300-2200 cm, Source B: 13000-22000 mm)
- Required fields (name, value, unitCode, sosa:resultTime)
- Unit code validation (CMT or MMT)
- WGS84 coordinate validation (latitude/longitude)

**Validation Note**: The data uses JSON-LD `@context` to map property names to URIs 
(e.g., `measuredAt` → `sosa:resultTime`). Your SHACL validator must expand the JSON-LD 
to RDF before validation. Tools like pySHACL handle this automatically:

```python
# Example with pySHACL (Python)
from pyshacl import validate
import requests

data = requests.get('http://localhost:8000/api/v1/source-a/current').json()
shapes = requests.get('http://localhost:8000/api/v1/shapes/shacl').json()

# pySHACL will automatically expand the @context
conforms, results_graph, results_text = validate(
    data_graph=data,
    shacl_graph=shapes,
    data_graph_format='json-ld',
    shacl_graph_format='json-ld'
)
print(f"Validation result: {conforms}")
```

### ODRL Policies
Visit http://localhost:8000/api/v1/shapes/odrl to see usage policies:
- Open access for everyone (public domain-like)
- Permitted actions: use, read, reproduce, distribute, derive, commercialize
- No restrictions or requirements

### DCAT-AP Catalog
Visit http://localhost:8000/api/v1/catalog for DCAT-AP compliant data catalog:
- European standard for data portals (DCAT-AP)
- Dataset descriptions with distributions
- Publisher and contact information
- Themes from EU controlled vocabularies (ENVI, Hydrography)
- Temporal and spatial coverage
- Conformance to SOSA/SSN, ISO, and INSPIRE standards

## Troubleshooting

### API won't start
- Make sure you installed dependencies: `py -m pip install -r requirements.txt`
- Check if port 8000 is already in use
- Verify Python version is 3.9 or higher: `py --version`

### Frontend can't connect to API
- Verify API is running at http://localhost:8000
- Check browser console for CORS errors
- Make sure you're accessing frontend via http:// (not file://)

### No data showing
- Open browser developer tools (F12)
- Check Console tab for errors
- Verify API is returning data: http://localhost:8000/api/v1/source-a/current
- Make sure auto-refresh is enabled (checkbox should be checked)

## Next Steps

- Explore the interactive API docs at http://localhost:8000/docs
- Examine the SHACL shapes and ODRL policies
- Test the primary source selection feature
- View water level threshold highlighting in action
- Modify the frontend styling in `frontend/css/styles.css`
- Add more sources in `api/routers/sources.py`
- Extend the SHACL shapes with additional constraints
- Experiment with different standard vocabularies (SOSA, Dublin Core)
