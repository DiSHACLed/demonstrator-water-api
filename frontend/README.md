# Frontend Deployment

This directory contains the DiSHACLed frontend web application.

## Files

- **index.html** - Main HTML interface
- **app.py** - Flask server for Azure App Service deployment
- **requirements.txt** - Python dependencies for Azure deployment
- **css/** - Stylesheets
- **js/** - JavaScript application logic

## Local Development

For local development, you can:

1. **Open directly in browser**:
   - Open `index.html` in your web browser
   - Update `js/app.js` to use local API: `const API_BASE_URL = 'http://localhost:8000/api/v1';`

2. **Use Python HTTP server**:
   ```bash
   python -m http.server 3000
   ```
   Then visit http://localhost:3000

## Azure Deployment

The frontend is deployed as a Python web app using Flask and Gunicorn.

### Deployment Files

**app.py** - Simple Flask application that serves static files:
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

**requirements.txt**:
```
flask==3.0.0
gunicorn==21.2.0
```

**Azure Startup Command**: `gunicorn -w 2 app:app`

### Configuration

The API endpoint is configured in `js/app.js`:

For **Azure** (production):
```javascript
const API_BASE_URL = 'https://dishacled-api.azurewebsites.net/api/v1';
```

For **Local development**:
```javascript
const API_BASE_URL = 'http://localhost:8000/api/v1';
```

### Deploy to Azure

From the project root:
```bash
cd frontend
az webapp up --resource-group dishacled-rg --name dishacled-frontend --runtime "PYTHON:3.11" --sku B1 --location westeurope
cd ..
```

## Live Deployment

The frontend is live at: https://dishacled-frontend.azurewebsites.net

## Technologies

- HTML5
- CSS3 (with custom gradients and responsive design)
- Vanilla JavaScript (ES6+)
- Flask (for Azure deployment only)
- Gunicorn (WSGI server for production)
