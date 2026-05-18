from fastapi import APIRouter
from datetime import datetime, timezone
from api.models import WaterLevelReading
import random
import time

router = APIRouter()

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


@router.get(
    "/source-a/current",
    responses={
        200: {
            "description": "Current water level from Source A in JSON-LD format. Unit code 'CMT' (centimetre) follows UN/CEFACT Common Code standard.",
            "content": {
                "application/json": {
                    "example": {
                        "@context": {
                            "@vocab": "https://schema.org/",
                            "sosa": "http://www.w3.org/ns/sosa/",
                            "dcterms": "http://purl.org/dc/terms/",
                            "measuredAt": "sosa:resultTime",
                            "conformsTo": "dcterms:conformsTo",
                            "source": "https://schema.org/source",
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
                }
            }
        }
    }
)
async def get_source_a_current():
    """
    Get current water level from Source A (in centimeters)
    
    Returns JSON-LD formatted water level measurement
    """
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
        location=SENSOR_LOCATION
    )
    return reading.model_dump(by_alias=True)


@router.get(
    "/source-b/current",
    responses={
        200: {
            "description": "Current water level from Source B in JSON-LD format. Unit code 'MMT' (millimetre) follows UN/CEFACT Common Code standard.",
            "content": {
                "application/json": {
                    "example": {
                        "@context": {
                            "@vocab": "https://schema.org/",
                            "sosa": "http://www.w3.org/ns/sosa/",
                            "dcterms": "http://purl.org/dc/terms/",
                            "measuredAt": "sosa:resultTime",
                            "conformsTo": "dcterms:conformsTo",
                            "source": "https://schema.org/source"
                        },
                        "@type": "PropertyValue",
                        "@id": "urn:measurement:source-b:2026-03-25T14:30:00",
                        "name": "Water Level - Source B",
                        "value": 17505.0,
                        "unitCode": "MMT",
                        "measuredAt": "2026-03-25T14:30:00Z",
                        "source": "Source B",
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
                }
            }
        }
    }
)
async def get_source_b_current():
    """
    Get current water level from Source B (in millimeters)
    
    Returns JSON-LD formatted water level measurement
    """
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
        location=SENSOR_LOCATION
    )
    return reading.model_dump(by_alias=True)


@router.get("/sources/all")
async def get_all_sources():
    """
    Get current readings from all sources
    
    Returns a JSON-LD collection of all measurements
    """
    source_a = await get_source_a_current()
    source_b = await get_source_b_current()
    
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


@router.get(
    "/antwerp/current",
    responses={
        200: {
            "description": "Current water level from Antwerp (proxy to active source) in JSON-LD format",
            "content": {
                "application/json": {
                    "example": {
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
                        "source": "Source A"
                    }
                }
            }
        }
    }
)
async def get_antwerp_current():
    """
    Get current water level from Antwerp (proxy to active source)
    
    Returns data from whichever source is currently marked as active.
    This endpoint acts as a single authoritative source by delegating 
    to either Source A or Source B based on the active source setting.
    """
    if active_source["name"] == "source-a":
        return await get_source_a_current()
    else:
        return await get_source_b_current()
