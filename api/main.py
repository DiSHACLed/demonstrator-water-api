from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import sources, sources_v2, control, metadata

app = FastAPI(
    title="DiSHACLed API",
    description=(
        "Water Level Monitoring Demo with JSON-LD and SHACL.\n\n"
        "**Measurement API versions**\n\n"
        "- **v1** (`/api/v1/...`): readings as schema.org `PropertyValue` JSON-LD "
        "(unit codes `CMT`/`MMT`).\n"
        "- **v2** (`/api/v2/...`): the same readings, driven by the same controls, "
        "represented as `sosa:Observation` \u2192 `qudt:QuantityValue` JSON-LD "
        "(QUDT units `unit:CentiM`/`unit:MilliM`).\n\n"
        "Both versions share the same water-level slider and active-source toggle, "
        "so they always stay synchronized.\n\n"
        "Measurement endpoints return JSON-LD and are served with the "
        "`application/ld+json` media type by default (content-negotiable: a client "
        "requesting only `application/json` still receives that content type)."
    ),
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
app.include_router(sources_v2.router, prefix="/api/v2", tags=["Water Sources (v2 SOSA/QUDT)"])
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
            "source_a_v2": "/api/v2/source-a/current",
            "source_b_v2": "/api/v2/source-b/current",
            "antwerp_v2": "/api/v2/antwerp/current",
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
