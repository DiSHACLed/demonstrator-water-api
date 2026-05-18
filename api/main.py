from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import sources, control, metadata

app = FastAPI(
    title="DiSHACLed API",
    description="Water Level Monitoring Demo with JSON-LD and SHACL",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sources.router, prefix="/api/v1", tags=["Water Sources"])
app.include_router(control.router, prefix="/api/v1/control", tags=["Control"])
app.include_router(metadata.router, prefix="/api/v1", tags=["Metadata"])


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "@context": "https://schema.org/",
        "@type": "WebAPI",
        "name": "DiSHACLed API",
        "description": "Water Level Monitoring Demo with Semantic Web Technologies",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "source_a": "/api/v1/source-a/current",
            "source_b": "/api/v1/source-b/current",
            "antwerp": "/api/v1/antwerp/current",
            "control": "/api/v1/control/set-level",
            "shacl": "/api/v1/shapes/shacl",
            "odrl": "/api/v1/shapes/odrl",
            "dcat_catalog": "/api/v1/catalog",
            "metadata": "/api/v1/metadata"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
