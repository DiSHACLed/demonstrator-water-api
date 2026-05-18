from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Literal


class WaterLevelReading(BaseModel):
    """Model for water level readings with JSON-LD context
    
    Unit codes follow the UN/CEFACT Common Code standard (Rec 20):
    - CMT: centimetre
    - MMT: millimetre
    See: https://unece.org/trade/cefact/UNLOCODE-Download
    """
    context: dict = Field(
        default={
            "@vocab": "https://schema.org/",
            "sosa": "http://www.w3.org/ns/sosa/",
            "dcterms": "http://purl.org/dc/terms/",
            "measuredAt": "sosa:resultTime",
            "conformsTo": "dcterms:conformsTo",
            "source": "https://schema.org/source"
        },
        alias="@context"
    )
    type: str = Field(default="PropertyValue", alias="@type")
    identifier: str = Field(alias="@id")
    name: str
    value: float
    unit_code: str = Field(alias="unitCode")
    measured_at: datetime = Field(alias="measuredAt")
    source: str
    location: Optional[dict] = None
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
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
                "name": "Water Level",
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
                    },
                    "address": {
                        "@type": "PostalAddress",
                        "addressLocality": "Antwerp",
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
                            "@id": "http://inspire.ec.europa.eu/id/citation/ir/reg-1089-2010",
                            "name": "Commission Regulation (EU) No 1089/2010"
                        },
                        {
                            "@type": "Standard",
                            "@id": "http://inspire.ec.europa.eu/theme/hy",
                            "name": "INSPIRE Data Specification on Hydrography"
                        },
                        {
                            "@type": "Standard",
                            "@id": "https://www.iso.org/standard/72004.html",
                            "name": "ISO 748: Hydrometry"
                        },
                        {
                            "@type": "Standard",
                            "@id": "https://www.iso.org/standard/44361.html",
                            "name": "ISO 1100: Hydrometry"
                        }
                    ]
                }
            }
        }
    )


class WaterLevelControl(BaseModel):
    """Model for controlling water levels"""
    level_percentage: float = Field(
        ge=0, 
        le=100, 
        description="Water level as percentage (0-100)"
    )


class ActiveSourceControl(BaseModel):
    """Model for setting the active water source"""
    source_name: str = Field(
        description="Name of the active source ('source-a' or 'source-b')"
    )


class ServiceMetadata(BaseModel):
    """Model for service metadata"""
    context: dict = Field(alias="@context")
    type: str = Field(alias="@type")
    identifier: str = Field(alias="@id")
    name: str
    description: str
    provider: dict
    dataset: dict
    
    class Config:
        populate_by_name = True
