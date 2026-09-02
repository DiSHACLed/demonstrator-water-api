from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timezone
from api.models import WaterLevelReading
import random
import time

router = APIRouter()


def _negotiate_measurement_response(request: Request, data: dict) -> Response:
    """Serialize a measurement as JSON-LD with a content-negotiated media type.

    These endpoints return JSON-LD bodies, so the response is labelled
    ``application/ld+json`` by default. This lets RDF toolchains consume the
    payload directly, without a JSON->JSON-LD workaround. If a client explicitly
    requests only ``application/json`` (without ld+json), that is honored for
    backward compatibility.
    """
    accept = request.headers.get("accept", "")
    if "application/ld+json" in accept:
        media_type = "application/ld+json"
    elif "application/json" in accept:
        media_type = "application/json"
    else:
        media_type = "application/ld+json"
    return JSONResponse(content=jsonable_encoder(data), media_type=media_type)

# Shared state for water level (controlled by the slider)
# Default to 30%
current_water_level = {"percentage": 30.0}

# Active source selection ("source-a" or "source-b")
active_source = {"name": "source-a"}

# Cache for base level to ensure both sources get the same value
# Values automatically recalculate every 5 seconds with new variation
_base_level_cache = {"value": 30.0, "last_update": time.time()}

# Sensor location in Antwerp
# Coordinates: 51°13'20.2"N 4°23'45.6"E (WGS84)
SENSOR_LOCATION = {
    "@type": "Place",
    "name": "Antwerp Water Monitoring Station",
    "geo": {
        "@type": "GeoCoordinates",
        "latitude": 51.222278,
        "longitude": 4.396
    },
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Antwerp",
        "addressRegion": "Flanders",
        "addressCountry": "BE"
    },
    "conformsTo": [
        {
            "@type": "Standard",
            "@id": "https://www.iso.org/standard/53798.html",
            "name": "ISO 19115-1:2014 Geographic information - Metadata"
        },
        {
            "@type": "Standard",
            "@id": "https://www.iso.org/standard/32579.html",
            "name": "ISO/TS 19139:2007 Geographic information - Metadata - XML schema implementation"
        },
        {
            "@type": "Standard",
            "@id": "http://inspire.ec.europa.eu/id/citation/ir/reg-1089-2010",
            "name": "Commission Regulation (EU) No 1089/2010 (Interoperability of spatial data sets and services)",
            "inLanguage": "en"
        },
        {
            "@type": "Standard",
            "@id": "http://inspire.ec.europa.eu/theme/hy",
            "name": "INSPIRE Data Specification on Hydrography",
            "inLanguage": "en"
        },
        {
            "@type": "Standard",
            "@id": "https://www.iso.org/standard/72004.html",
            "name": "ISO 748: Hydrometry - Measurement of liquid flow in open channels",
            "inLanguage": "en"
        },
        {
            "@type": "Standard",
            "@id": "https://www.iso.org/standard/44361.html",
            "name": "ISO 1100: Hydrometry - Measurement of liquid flow in open channels (Stage-discharge relation)",
            "inLanguage": "en"
        }
    ]
}


def get_base_level():
    """Get base water level from control state
    
    Automatically recalculates every 5 seconds with new random variation.
    Returns the same value for both sources within the same time window,
    ensuring Source A and Source B always show synchronized readings.
    """
    current_time = time.time()
    
    # Recalculate if 5 seconds have passed since last update
    if current_time - _base_level_cache["last_update"] >= 5.0:
        # Update timestamp FIRST to prevent race conditions
        # (other concurrent requests will see the new timestamp and skip recalculation)
        _base_level_cache["last_update"] = current_time
        
        level = current_water_level["percentage"]
        
        # Add some random variation for realism (±2%)
        variation = random.uniform(-2, 2)
        
        _base_level_cache["value"] = max(0, min(100, level + variation))
    
    return _base_level_cache["value"]


def _build_source_a_reading() -> dict:
    """Build the Source A water-level reading as a JSON-LD dict (centimetres)."""
    base_level = get_base_level()
    # Convert percentage to cm (13-22 meters)
    value_cm = 1300 + (base_level * 9.0)
    timestamp = datetime.now(timezone.utc)
    reading = WaterLevelReading(
        identifier=f"urn:measurement:source-a:{timestamp.isoformat()}",
        name="Water Level - Source A",
        value=round(value_cm, 2),
        unit_code="CMT",  # Centimeter
        measured_at=timestamp,
        source="Source A",
        sensor_brand="HydroMeasureX5",
        location=SENSOR_LOCATION
    )
    return reading.model_dump(by_alias=True)


def _build_source_b_reading() -> dict:
    """Build the Source B water-level reading as a JSON-LD dict (millimetres)."""
    base_level = get_base_level()
    # Convert percentage to mm (13-22 meters)
    value_mm = 13000 + (base_level * 90.0)
    timestamp = datetime.now(timezone.utc)
    reading = WaterLevelReading(
        identifier=f"urn:measurement:source-b:{timestamp.isoformat()}",
        name="Water Level - Source B",
        value=round(value_mm, 2),
        unit_code="MMT",  # Millimeter
        measured_at=timestamp,
        source="Source B",
        sensor_brand="WaterProber3",
        location=SENSOR_LOCATION
    )
    data = reading.model_dump(by_alias=True)
    # Source B additionally reports water temperature (Source A does not).
    data["waterTemperature"] = "18°C"
    return data


# OpenAPI response examples. Advertised under both ``application/ld+json`` (the
# default media type actually served) and ``application/json`` (accepted for
# backward compatibility via content negotiation).
_SOURCE_A_EXAMPLE = {
    "@context": {
        "@vocab": "https://schema.org/",
        "sosa": "http://www.w3.org/ns/sosa/",
        "dcterms": "http://purl.org/dc/terms/",
        "measuredAt": "sosa:resultTime",
        "conformsTo": "dcterms:conformsTo",
        "source": "https://schema.org/source",
    },
    "@type": "PropertyValue",
    "@id": "urn:measurement:source-a:2026-03-25T10:30:00",
    "name": "Water Level - Source A",
    "value": 1750.5,
    "unitCode": "CMT",
    "measuredAt": "2026-03-25T10:30:00Z",
    "source": "Source A",
    "SensorBrand": "HydroMeasureX5",
    "location": {
        "@type": "Place",
        "name": "Antwerp Water Monitoring Station",
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 51.222278,
            "longitude": 4.396,
        },
    },
}

_SOURCE_B_EXAMPLE = {
    "@context": {
        "@vocab": "https://schema.org/",
        "sosa": "http://www.w3.org/ns/sosa/",
        "dcterms": "http://purl.org/dc/terms/",
        "measuredAt": "sosa:resultTime",
        "conformsTo": "dcterms:conformsTo",
        "source": "https://schema.org/source",
    },
    "@type": "PropertyValue",
    "@id": "urn:measurement:source-b:2026-03-25T14:30:00",
    "name": "Water Level - Source B",
    "value": 17505.0,
    "unitCode": "MMT",
    "measuredAt": "2026-03-25T14:30:00Z",
    "source": "Source B",
    "SensorBrand": "WaterProber3",
    "waterTemperature": "18°C",
    "location": {
        "@type": "Place",
        "name": "Antwerp Water Monitoring Station",
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 51.222278,
            "longitude": 4.396,
        },
    },
}

_ANTWERP_EXAMPLE = {
    "@context": {
        "@vocab": "https://schema.org/",
        "sosa": "http://www.w3.org/ns/sosa/",
        "dcterms": "http://purl.org/dc/terms/",
        "measuredAt": "sosa:resultTime",
        "conformsTo": "dcterms:conformsTo",
        "source": "https://schema.org/source",
    },
    "@type": "PropertyValue",
    "@id": "urn:measurement:source-a:2026-03-25T10:30:00",
    "name": "Water Level - Source A",
    "value": 1750.5,
    "unitCode": "CMT",
    "measuredAt": "2026-03-25T10:30:00Z",
    "source": "Source A",
    "SensorBrand": "HydroMeasureX5",
}


@router.api_route(
    "/source-a/current",
    methods=["GET", "HEAD"],
    responses={
        200: {
            "description": "Current water level from Source A in JSON-LD format. Unit code 'CMT' (centimetre) follows UN/CEFACT Common Code standard.",
            "content": {
                "application/ld+json": {"example": _SOURCE_A_EXAMPLE},
                "application/json": {"example": _SOURCE_A_EXAMPLE},
            }
        }
    }
)
async def get_source_a_current(request: Request):
    """
    Get current water level from Source A (in centimeters)

    Returns a JSON-LD water level measurement served as
    ``application/ld+json`` (content-negotiable).
    """
    return _negotiate_measurement_response(request, _build_source_a_reading())


@router.api_route(
    "/source-b/current",
    methods=["GET", "HEAD"],
    responses={
        200: {
            "description": "Current water level from Source B in JSON-LD format. Unit code 'MMT' (millimetre) follows UN/CEFACT Common Code standard.",
            "content": {
                "application/ld+json": {"example": _SOURCE_B_EXAMPLE},
                "application/json": {"example": _SOURCE_B_EXAMPLE},
            }
        }
    }
)
async def get_source_b_current(request: Request):
    """
    Get current water level from Source B (in millimeters)

    Returns a JSON-LD water level measurement served as
    ``application/ld+json`` (content-negotiable).
    """
    return _negotiate_measurement_response(request, _build_source_b_reading())


@router.get("/sources/all")
async def get_all_sources():
    """
    Get current readings from all sources
    
    Returns a JSON-LD collection of all measurements
    """
    source_a = _build_source_a_reading()
    source_b = _build_source_b_reading()
    
    return {
        "@context": "https://schema.org/",
        "@type": "ItemList",
        "name": "All Water Level Sources",
        "numberOfItems": 2,
        "itemListElement": [
            source_a,
            source_b
        ]
    }


@router.api_route(
    "/antwerp/current",
    methods=["GET", "HEAD"],
    responses={
        200: {
            "description": "Current water level from Antwerp (proxy to active source) in JSON-LD format",
            "content": {
                "application/ld+json": {"example": _ANTWERP_EXAMPLE},
                "application/json": {"example": _ANTWERP_EXAMPLE},
            }
        }
    }
)
async def get_antwerp_current(request: Request):
    """
    Get current water level from Antwerp (proxy to active source)

    Returns data from whichever source is currently marked as active.
    This endpoint acts as a single authoritative source by delegating
    to either Source A or Source B based on the active source setting.
    Served as ``application/ld+json`` (content-negotiable).
    """
    if active_source["name"] == "source-a":
        data = _build_source_a_reading()
    else:
        data = _build_source_b_reading()
    return _negotiate_measurement_response(request, data)
