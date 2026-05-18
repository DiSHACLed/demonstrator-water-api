# DiSHACLed Project Overview

## � Live Deployment

**The application is deployed and running on Azure:**
- Frontend: https://dishacled-frontend.azurewebsites.net
- API: https://dishacled-api.azurewebsites.net
- API Docs: https://dishacled-api.azurewebsites.net/docs

## �🎯 What You Have

A complete, working demonstration system for semantic water level monitoring featuring:

### ✅ Backend API (Python FastAPI)
- **Mocked water level endpoints** for two sources
  - Source A: Publishes in centimeters (1300-2200 cm)
  - Source B: Publishes in millimeters (13000-22000 mm)
  - Both sources synchronized - B value always exactly 10× A value
  - Antwerp: Proxy endpoint using active primary source
- **Automatic updates** every 5 seconds with ±2% realistic variation
- **Race condition protection** via timestamp-first cache updates
- **Single-worker deployment** to maintain consistent shared state
- **Control API** to adjust water levels and set active source
- **Semantic metadata** with SHACL shapes and ODRL policies
- **JSON-LD formatted** responses with standard vocabularies (SOSA, Dublin Core)
- **Auto-generated API documentation** at `/docs`

### ✅ Frontend (Vanilla HTML/CSS/JavaScript)
- **Visual slider control** to adjust water level (0-100%)
- **Primary source selector** (radio buttons for Source A/B)
- **Water level thresholds table** with 5 warning levels
- **Real-time data display** from both sources
- **Auto-refresh** every 5 seconds (synchronized with backend updates)
- **Beautiful, responsive design** with gradient cards
- **Quick access** to SHACL, ODRL, and metadata endpoints

### ✅ Semantic Web Integration
- **SHACL Shapes** for data validation
- **ODRL Policies** for usage rights
- **DCAT-AP Catalog** describing datasets and distributions in European standard format
- **JSON-LD context** on all responses with WGS84 coordinates

## 📁 Project Structure

```
DiSHACLed/
│
├── api/                          # FastAPI Backend
│   ├── main.py                   # Main application with CORS
│   ├── models.py                 # Pydantic models for validation
│   ├── __init__.py
│   └── routers/
│       ├── sources.py            # Water source endpoints
│       ├── control.py            # Control endpoints
│       ├── metadata.py           # SHACL/ODRL/metadata
│       └── __init__.py
│
├── frontend/                     # Web Interface
│   ├── index.html                # Main UI
│   ├── app.py                    # Flask server for Azure
│   ├── requirements.txt          # Frontend Python dependencies
│   ├── css/
│   │   └── styles.css            # Beautiful styling
│   └── js/
│       └── app.js                # Frontend logic (configured for Azure API)
│
├── README.md                     # Project documentation
├── QUICKSTART.md                 # Detailed setup guide
├── PROJECT_OVERVIEW.md           # This file
├── requirements.txt              # API Python dependencies (includes Gunicorn)
├── .gitignore                    # Git ignore rules
│
├── start.ps1                     # Start everything (local dev)
├── start-api.ps1                 # Start API only (local dev)
└── start-frontend.ps1            # Start frontend only (local dev)
```

## 🚀 Quick Start Options

### Option 1: Use the Live Deployment (Fastest)

Just visit:
- **Control Center**: https://dishacled-frontend.azurewebsites.net
- **API Docs**: https://dishacled-api.azurewebsites.net/docs

No installation required!

### Option 2: Run Locally (3 Steps)

#### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

#### 2. Start Everything
```powershell
.\start.ps1
```

This opens two terminal windows (API + Frontend) and launches your browser!

#### 3. Use the Control Center
- Adjust the slider to change water levels
- Select primary source (A or B) for Antwerp endpoint
- View water level thresholds with real-time highlighting
- Watch real-time data update automatically

### Option 3: Deploy to Your Own Azure

```powershell
# Set your subscription
az account set --subscription YOUR_SUBSCRIPTION_ID

# Deploy API
az webapp up --resource-group YOUR_RG --name YOUR_API_NAME --runtime "PYTHON:3.11" --sku B1 --location westeurope

# Deploy Frontend (update js/app.js with your API URL first)
cd frontend
az webapp up --resource-group YOUR_RG --name YOUR_FRONTEND_NAME --runtime "PYTHON:3.11" --sku B1 --location westeurope
```

## 🔌 API Endpoints

### Water Sources
- `GET /api/v1/source-a/current` - Current reading from Source A (1300-2200 cm)
- `GET /api/v1/source-b/current` - Current reading from Source B (13000-22000 mm)
- `GET /api/v1/antwerp/current` - Antwerp proxy using active primary source
- `GET /api/v1/sources/all` - All sources in JSON-LD collection

### Control
- `POST /api/v1/control/set-level` - Set water level (0-100%)
- `POST /api/v1/control/set-active-source` - Set primary source (source-a or source-b)
- `GET /api/v1/control/active-source` - Get current active source
- `GET /api/v1/control/current-settings` - Get current control settings

### Metadata
- `GET /api/v1/shapes/shacl` - SHACL validation shapes
- `GET /api/v1/shapes/odrl` - ODRL usage policies
- `GET /api/v1/catalog` - DCAT-AP data catalog
- `GET /api/v1/metadata` - Service metadata (legacy)
- `GET /docs` - Interactive API documentation

## 🎨 Key Features

### Backend Features
✅ **JSON-LD Support** - All responses use semantic web standards
✅ **CORS Enabled** - Frontend can access API from any origin
✅ **Auto-reload** - Changes to code reload automatically
✅ **Mock Data** - Realistic water level simulations with variation
✅ **Synchronized Sources** - Perfect 10:1 ratio maintained between A and B
✅ **Time-based Caching** - 5-second windows ensure consistent values
✅ **FastAPI Docs** - Built-in Swagger UI at `/docs`

### Frontend Features
✅ **Responsive Design** - Works on desktop and mobile
✅ **Real-time Updates** - Auto-refresh every 5 seconds
✅ **Perfect Synchronization** - Source A and B always show same measurement (different units)
✅ **Cache-Busting** - Frontend includes no-cache headers to prevent stale data
✅ **Visual Feedback** - Animated status indicators
✅ **Error Handling** - Graceful error display
✅ **Gradient Cards** - Beautiful visual design
✅ **Warning System** - Alerts for high water levels

## 🌐 Semantic Web Components

### SHACL Shapes
Defines validation constraints:
- Required properties (name, value, unitCode, sosa:resultTime)
- Data types (xsd:decimal for value, coordinates)
- Value ranges (1300-2200 for Source A, 13000-22000 for Source B)
- Unit code validation (CMT or MMT from UN/CEFACT Common Code standard)
- WGS84 coordinate validation

### ODRL Policies
Defines usage rights:
- **Open Access**: Public can freely use, read, reproduce, distribute, derive, and commercialize
- **No Restrictions**: No prohibitions or requirements
- **Assignee**: General public (http://www.w3.org/ns/odrl/2/Public)

### DCAT-AP Catalog
European standard data catalog:
- Dataset information with JSON-LD distributions
- Publisher details (FOAF)
- WGS84 coordinates for Antwerp sensor location
- ISO standards and INSPIRE conformance declarations
- SOSA/SSN ontology for sensor observations
- Keywords and themes from EU controlled vocabularies
- Contact points using vCard
- Temporal and spatial coverage

## 🎬 Demo Scenarios

### Normal Monitoring
1. Start with default 30% level (~1570 cm / ~15700 mm)
2. View synchronized readings from both sources
3. Notice Source B = Source A × 10 (unit conversion)
4. See water level thresholds table with highlighted current level

### Simulating Water Level Changes
1. Move slider from 30% to 70% (~1930 cm / ~19300 mm)
2. Watch values increase proportionally
3. See threshold highlighting change in real-time
4. Values include ±2% random variation for realism

### Primary Source Selection
1. View current Antwerp endpoint value
2. Switch between Source A and Source B using radio buttons
3. Click "Set as Primary"
4. Antwerp endpoint now returns data from selected source
5. Useful for demonstrating source priority/failover

## 🔧 Customization Ideas

### Backend Extensions
- Add more water sources (Source C, D, etc.)
- Implement historical data storage
- Add WebSocket support for true real-time streaming
- Create validation endpoint that uses SHACL to validate incoming data
- Add authentication/authorization

### Frontend Enhancements
- Add charts/graphs for historical trends
- Create map view showing source locations
- Add alert notifications for threshold violations
- Implement dark mode
- Add export functionality (CSV, JSON-LD)

### Semantic Enhancements
- Add more detailed SHACL constraints
- Create SPARQL query endpoint
- Integrate with RDF triple store
- Add provenance information (PROV-O)
- Implement linked data principles with dereferenceable URIs

## 📚 Technologies Used

### Backend Stack
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation using Python type hints
- **Uvicorn** - ASGI server for FastAPI
- **Python-multipart** - Form data handling

### Frontend Stack
- **Vanilla JavaScript** - No framework dependencies
- **CSS3** - Modern styling with gradients and animations
- **HTML5** - Semantic markup

### Semantic Web
- **JSON-LD** - Linked Data format
- **SHACL** - Shapes Constraint Language  
- **ODRL** - Open Digital Rights Language
- **DCAT-AP** - Data Catalog Vocabulary Application Profile (European standard)
- **Schema.org** - Vocabulary for semantic markup
- **SOSA/SSN** - Sensor Network Ontology (W3C)
- **Dublin Core Terms** - Metadata vocabulary
- **FOAF** - Friend of a Friend vocabulary
- **vCard** - Contact information vocabulary

### JSON-LD
- https://json-ld.org/
- https://www.w3.org/TR/json-ld11/

### SHACL
- https://www.w3.org/TR/shacl/
- https://datashapes.org/

### ODRL
- https://www.w3.org/TR/odrl-model/
- https://www.w3.org/community/odrl/

### DCAT-AP
- https://www.w3.org/TR/vocab-dcat-3/
- https://joinup.ec.europa.eu/collection/semantic-interoperability-community-semic/solution/dcat-application-profile-data-portals-europe
- https://semiceu.github.io/DCAT-AP/releases/

### FastAPI
- https://fastapi.tiangolo.com/

## 💡 Tips

1. **Use the interactive docs**: Visit http://localhost:8000/docs to test API endpoints
2. **Check browser console**: Press F12 to see what's happening behind the scenes
3. **Monitor API logs**: Watch the API terminal for request/response logs
4. **Test with curl**: Use the examples in QUICKSTART.md
5. **Modify and experiment**: The code is well-structured and commented

## 🐛 Common Issues

**"uvicorn: command not found"**
→ Run `pip install -r requirements.txt`

**"Port 8000 already in use"**
→ Change port in start-api.ps1 or kill existing process

**"CORS error in browser"**
→ Make sure you're accessing via http:// and not file://

**"No data showing"**
→ Verify API is running at http://localhost:8000/api/v1/source-a/current

## 🎯 Next Steps

1. **Run it**: `.\start.ps1`
2. **Explore it**: Try the slider, check the metadata endpoints
3. **Understand it**: Read through the code, it's well commented
4. **Extend it**: Add your own features and ideas
5. **Present it**: Great demo for semantic web concepts!