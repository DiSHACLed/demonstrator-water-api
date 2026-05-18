# Deployment Checklist

Quick reference checklist for deploying DiSHACLed to Azure.

## ✅ Pre-Deployment

- [ ] Azure CLI installed: `az --version`
- [ ] Logged into Azure: `az login`
- [ ] Correct subscription selected: `az account show`
- [ ] Git repository is clean (optional): `git status`

## ✅ API Deployment

### 1. Prerequisites
- [ ] In project root directory
- [ ] `requirements.txt` includes `gunicorn==21.2.0`
- [ ] API code is working locally

### 2. Deploy
```bash
az webapp up --resource-group dishacled-rg \
  --name dishacled-api \
  --runtime "PYTHON:3.11" \
  --sku B1 \
  --location westeurope
```

### 3. Configure
- [ ] Startup command: `gunicorn -w 1 -k uvicorn.workers.UvicornWorker api.main:app` (single worker required)
  ```bash
  az webapp config set --resource-group dishacled-rg \
    --name dishacled-api \
    --startup-file "gunicorn -w 1 -k uvicorn.workers.UvicornWorker api.main:app"
  ```

### 4. Verify
- [ ] Check status: `az webapp show --name dishacled-api --resource-group dishacled-rg`
- [ ] Test endpoint: https://dishacled-api.azurewebsites.net/
- [ ] Check docs: https://dishacled-api.azurewebsites.net/docs
- [ ] View logs: `az webapp log tail --name dishacled-api --resource-group dishacled-rg`

## ✅ Frontend Deployment

### 1. Prerequisites
- [ ] In project root directory
- [ ] `frontend/app.py` exists
- [ ] `frontend/requirements.txt` includes Flask and Gunicorn
- [ ] API URL updated in `frontend/js/app.js`:
  ```javascript
  const API_BASE_URL = 'https://dishacled-api.azurewebsites.net/api/v1';
  ```

### 2. Deploy
```bash
cd frontend
az webapp up --resource-group dishacled-rg \
  --name dishacled-frontend \
  --runtime "PYTHON:3.11" \
  --sku B1 \
  --location westeurope
cd ..
```

### 3. Configure
- [ ] Startup command: `gunicorn -w 2 app:app`
  ```bash
  az webapp config set --resource-group dishacled-rg \
    --name dishacled-frontend \
    --startup-file "gunicorn -w 2 app:app"
  ```

### 4. Verify
- [ ] Check status: `az webapp show --name dishacled-frontend --resource-group dishacled-rg`
- [ ] Test endpoint: https://dishacled-frontend.azurewebsites.net/
- [ ] Test functionality: Use slider and verify data updates
- [ ] View logs: `az webapp log tail --name dishacled-frontend --resource-group dishacled-rg`

## ✅ Post-Deployment

### Testing
- [ ] Visit frontend: https://dishacled-frontend.azurewebsites.net
- [ ] Adjust water level slider (0-100%)
- [ ] Toggle between Source A and Source B
- [ ] Verify real-time data updates
- [ ] Check threshold highlighting works
- [ ] Test API docs: https://dishacled-api.azurewebsites.net/docs
- [ ] Test all API endpoints via Swagger UI

### Monitoring
- [ ] Enable logging:
  ```bash
  az webapp log config --resource-group dishacled-rg \
    --name dishacled-api \
    --application-logging filesystem \
    --level information
    
  az webapp log config --resource-group dishacled-rg \
    --name dishacled-frontend \
    --application-logging filesystem \
    --level information
  ```
- [ ] Set up alerts (optional)
- [ ] Configure Application Insights (optional)

### Security (Optional)
- [ ] Enable HTTPS only:
  ```bash
  az webapp update --resource-group dishacled-rg \
    --name dishacled-api --https-only true
    
  az webapp update --resource-group dishacled-rg \
    --name dishacled-frontend --https-only true
  ```
- [ ] Restrict CORS to frontend domain in `api/main.py`
- [ ] Set up IP restrictions (if needed)

### Documentation
- [ ] Update `CHANGELOG.md` with deployment date/version
- [ ] Document any custom configurations
- [ ] Note deployment URLs in team documentation

## 🔄 Redeployment

To redeploy after making changes:

**API:**
```bash
az webapp up --resource-group dishacled-rg --name dishacled-api
```

**Frontend:**
```bash
cd frontend
az webapp up --resource-group dishacled-rg --name dishacled-frontend
cd ..
```

## 🆘 Troubleshooting

### Application won't start
- [ ] Check logs: `az webapp log tail --name dishacled-api --resource-group dishacled-rg`
- [ ] Verify startup command is correct
- [ ] Ensure all dependencies in requirements.txt
- [ ] Restart: `az webapp restart --name dishacled-api --resource-group dishacled-rg`

### Frontend can't connect to API
- [ ] Verify API URL in `frontend/js/app.js`
- [ ] Check CORS settings in `api/main.py`
- [ ] Test API directly in browser
- [ ] Check browser console for errors

### Deployment fails
- [ ] Verify Azure CLI authentication: `az account show`
- [ ] Check you're in correct directory
- [ ] Try with `--verbose` flag
- [ ] Check Azure portal for service health

## 📋 Quick Commands Reference

```bash
# View all resources
az resource list --resource-group dishacled-rg -o table

# Restart apps
az webapp restart --name dishacled-api --resource-group dishacled-rg
az webapp restart --name dishacled-frontend --resource-group dishacled-rg

# Stream logs
az webapp log tail --name dishacled-api --resource-group dishacled-rg
az webapp log tail --name dishacled-frontend --resource-group dishacled-rg

# Check app status
az webapp show --name dishacled-api --resource-group dishacled-rg \
  --query "{state:state, url:defaultHostName}" -o table

# Delete everything (careful!)
az group delete --name dishacled-rg --yes
```

## 📚 Documentation

For detailed information, see:
- [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md) - Complete deployment guide
- [QUICKSTART.md](QUICKSTART.md) - Development and deployment walkthrough
- [CHANGELOG.md](CHANGELOG.md) - Version history and changes

## 🎯 Success Criteria

Deployment is successful when:
- ✅ Frontend loads at https://dishacled-frontend.azurewebsites.net
- ✅ API responds at https://dishacled-api.azurewebsites.net
- ✅ API docs available at https://dishacled-api.azurewebsites.net/docs
- ✅ Slider adjusts water levels
- ✅ Source selector switches between A and B
- ✅ Real-time data updates every 5 seconds (synchronized with backend)
- ✅ Thresholds highlight appropriately
- ✅ No errors in browser console
- ✅ No errors in application logs
