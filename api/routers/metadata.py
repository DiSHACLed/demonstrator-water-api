from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/catalog")
async def get_dcat_catalog():
    """
    Get DCAT-AP catalog metadata
    
    Returns a DCAT-AP compliant catalog describing the water monitoring datasets
    and their distributions. DCAT-AP is the European standard for data portals.
    """
    return {
        "@context": {
            "@vocab": "http://www.w3.org/ns/dcat#",
            "dcat": "http://www.w3.org/ns/dcat#",
            "dcterms": "http://purl.org/dc/terms/",
            "foaf": "http://xmlns.com/foaf/0.1/",
            "vcard": "http://www.w3.org/2006/vcard/ns#",
            "schema": "https://schema.org/",
            "adms": "http://www.w3.org/ns/adms#",
            "spdx": "http://spdx.org/rdf/terms#"
        },
        "@id": "https://dishacled.example.org/catalog",
        "@type": "Catalog",
        "dcterms:title": {
            "@value": "DiSHACLed Water Monitoring Data Catalog",
            "@language": "en"
        },
        "dcterms:description": {
            "@value": "Open data catalog providing real-time water level measurements from Antwerp monitoring stations. Data is published as JSON-LD with semantic annotations using SOSA/SSN ontology.",
            "@language": "en"
        },
        "dcterms:publisher": {
            "@type": "foaf:Organization",
            "foaf:name": "DiSHACLed Project",
            "foaf:homepage": "https://dishacled.example.org"
        },
        "dcterms:issued": "2026-03-25",
        "dcterms:modified": "2026-03-25",
        "dcterms:language": "http://publications.europa.eu/resource/authority/language/ENG",
        "dcterms:license": "http://creativecommons.org/publicdomain/zero/1.0/",
        "foaf:homepage": "https://dishacled.example.org",
        "dataset": [
            {
                "@id": "https://dishacled.example.org/dataset/source-a",
                "@type": "Dataset",
                "dcterms:title": {
                    "@value": "Water Level Measurements - Source A",
                    "@language": "en"
                },
                "dcterms:description": {
                    "@value": "Real-time water level measurements from Source A in centimeters. Measurements range from 1300 to 2200 cm and are updated continuously.",
                    "@language": "en"
                },
                "dcterms:identifier": "source-a",
                "dcterms:issued": "2026-03-25",
                "dcterms:modified": "2026-03-25",
                "dcterms:publisher": {
                    "@type": "foaf:Organization",
                    "foaf:name": "DiSHACLed Project"
                },
                "dcterms:accrualPeriodicity": "http://publications.europa.eu/resource/authority/frequency/CONT",
                "dcterms:spatial": {
                    "@type": "dcterms:Location",
                    "schema:name": "Antwerp, Belgium",
                    "schema:geo": {
                        "@type": "schema:GeoCoordinates",
                        "schema:latitude": 51.222278,
                        "schema:longitude": 4.396
                    }
                },
                "dcterms:temporal": {
                    "@type": "dcterms:PeriodOfTime",
                    "schema:startDate": "2026-03-25"
                },
                "dcat:theme": [
                    "http://publications.europa.eu/resource/authority/data-theme/ENVI",
                    "http://inspire.ec.europa.eu/theme/hy"
                ],
                "dcat:keyword": [
                    {"@value": "water level", "@language": "en"},
                    {"@value": "hydrometry", "@language": "en"},
                    {"@value": "real-time", "@language": "en"},
                    {"@value": "sensor data", "@language": "en"}
                ],
                "dcat:contactPoint": {
                    "@type": "vcard:Organization",
                    "vcard:fn": "DiSHACLed Support",
                    "vcard:hasEmail": "mailto:contact@dishacled.example.org"
                },
                "dcterms:conformsTo": [
                    "https://www.w3.org/TR/vocab-ssn/",
                    "https://www.iso.org/standard/53798.html",
                    "http://inspire.ec.europa.eu/theme/hy"
                ],
                "dcat:distribution": [
                    {
                        "@id": "https://dishacled.example.org/distribution/source-a-jsonld",
                        "@type": "Distribution",
                        "dcterms:title": {
                            "@value": "Source A - JSON-LD API",
                            "@language": "en"
                        },
                        "dcterms:description": {
                            "@value": "Real-time JSON-LD endpoint providing current water level readings",
                            "@language": "en"
                        },
                        "dcat:accessURL": "https://dishacled-api.azurewebsites.net/api/v1/source-a/current",
                        "dcterms:format": "http://publications.europa.eu/resource/authority/file-type/JSON_LD",
                        "dcat:mediaType": "application/ld+json",
                        "dcterms:license": "http://creativecommons.org/publicdomain/zero/1.0/",
                        "adms:status": "http://purl.org/adms/status/Completed"
                    }
                ]
            },
            {
                "@id": "https://dishacled.example.org/dataset/source-b",
                "@type": "Dataset",
                "dcterms:title": {
                    "@value": "Water Level Measurements - Source B",
                    "@language": "en"
                },
                "dcterms:description": {
                    "@value": "Real-time water level measurements from Source B in millimeters. Measurements range from 13000 to 22000 mm and are updated continuously.",
                    "@language": "en"
                },
                "dcterms:identifier": "source-b",
                "dcterms:issued": "2026-03-25",
                "dcterms:modified": "2026-03-25",
                "dcterms:publisher": {
                    "@type": "foaf:Organization",
                    "foaf:name": "DiSHACLed Project"
                },
                "dcterms:accrualPeriodicity": "http://publications.europa.eu/resource/authority/frequency/CONT",
                "dcterms:spatial": {
                    "@type": "dcterms:Location",
                    "schema:name": "Antwerp, Belgium",
                    "schema:geo": {
                        "@type": "schema:GeoCoordinates",
                        "schema:latitude": 51.222278,
                        "schema:longitude": 4.396
                    }
                },
                "dcterms:temporal": {
                    "@type": "dcterms:PeriodOfTime",
                    "schema:startDate": "2026-03-25"
                },
                "dcat:theme": [
                    "http://publications.europa.eu/resource/authority/data-theme/ENVI",
                    "http://inspire.ec.europa.eu/theme/hy"
                ],
                "dcat:keyword": [
                    {"@value": "water level", "@language": "en"},
                    {"@value": "hydrometry", "@language": "en"},
                    {"@value": "real-time", "@language": "en"},
                    {"@value": "sensor data", "@language": "en"}
                ],
                "dcat:contactPoint": {
                    "@type": "vcard:Organization",
                    "vcard:fn": "DiSHACLed Support",
                    "vcard:hasEmail": "mailto:contact@dishacled.example.org"
                },
                "dcterms:conformsTo": [
                    "https://www.w3.org/TR/vocab-ssn/",
                    "https://www.iso.org/standard/53798.html",
                    "http://inspire.ec.europa.eu/theme/hy"
                ],
                "dcat:distribution": [
                    {
                        "@id": "https://dishacled.example.org/distribution/source-b-jsonld",
                        "@type": "Distribution",
                        "dcterms:title": {
                            "@value": "Source B - JSON-LD API",
                            "@language": "en"
                        },
                        "dcterms:description": {
                            "@value": "Real-time JSON-LD endpoint providing current water level readings",
                            "@language": "en"
                        },
                        "dcat:accessURL": "https://dishacled-api.azurewebsites.net/api/v1/source-b/current",
                        "dcterms:format": "http://publications.europa.eu/resource/authority/file-type/JSON_LD",
                        "dcat:mediaType": "application/ld+json",
                        "dcterms:license": "http://creativecommons.org/publicdomain/zero/1.0/",
                        "adms:status": "http://purl.org/adms/status/Completed"
                    }
                ]
            },
            {
                "@id": "https://dishacled.example.org/dataset/antwerp",
                "@type": "Dataset",
                "dcterms:title": {
                    "@value": "Water Level Measurements - Antwerp (Proxy)",
                    "@language": "en"
                },
                "dcterms:description": {
                    "@value": "Proxy endpoint that returns data from the currently configured primary source (either Source A or Source B).",
                    "@language": "en"
                },
                "dcterms:identifier": "antwerp",
                "dcterms:issued": "2026-03-25",
                "dcterms:modified": "2026-03-25",
                "dcterms:publisher": {
                    "@type": "foaf:Organization",
                    "foaf:name": "DiSHACLed Project"
                },
                "dcterms:accrualPeriodicity": "http://publications.europa.eu/resource/authority/frequency/CONT",
                "dcat:distribution": [
                    {
                        "@id": "https://dishacled.example.org/distribution/antwerp-jsonld",
                        "@type": "Distribution",
                        "dcterms:title": {
                            "@value": "Antwerp - JSON-LD API",
                            "@language": "en"
                        },
                        "dcat:accessURL": "https://dishacled-api.azurewebsites.net/api/v1/antwerp/current",
                        "dcterms:format": "http://publications.europa.eu/resource/authority/file-type/JSON_LD",
                        "dcat:mediaType": "application/ld+json",
                        "dcterms:license": "http://creativecommons.org/publicdomain/zero/1.0/"
                    }
                ]
            }
        ]
    }


@router.get("/metadata")
async def get_service_metadata():
    """
    Get service and dataset metadata
    
    Returns comprehensive metadata about the water monitoring service
    """
    return {
        "@context": {
            "@vocab": "https://schema.org/",
            "dcat": "http://www.w3.org/ns/dcat#",
            "dcterms": "http://purl.org/dc/terms/",
            "odrl": "http://www.w3.org/ns/odrl/2/"
        },
        "@type": "WebAPI",
        "@id": "urn:service:dishacled:water-monitoring",
        "name": "DiSHACLed Water Monitoring Service",
        "description": "Semantic water level monitoring service providing real-time measurements from multiple sources",
        "version": "1.0.0",
        "provider": {
            "@type": "Organization",
            "name": "DiSHACLed Project",
            "url": "https://example.org/dishacled"
        },
        "dataset": [
            {
                "@type": "Dataset",
                "@id": "urn:dataset:source-a",
                "name": "Source A Water Levels",
                "description": "Real-time water level measurements in centimeters",
                "distribution": {
                    "@type": "DataDownload",
                    "encodingFormat": "application/ld+json",
                    "contentUrl": "/api/v1/source-a/current"
                },
                "measurementTechnique": "Water level sensor",
                "variableMeasured": {
                    "@type": "PropertyValue",
                    "name": "Water Level",
                    "unitCode": "CMT"
                },
                "spatialCoverage": {
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
                    }
                },
                "conformsTo": [
                    "https://www.iso.org/standard/53798.html",
                    "ISO 19115-1:2014 Geographic information - Metadata",
                    "ISO/TS 19139:2007"
                ]
            },
            {
                "@type": "Dataset",
                "@id": "urn:dataset:source-b",
                "name": "Source B Water Levels",
                "description": "Real-time water level measurements in millimeters",
                "distribution": {
                    "@type": "DataDownload",
                    "encodingFormat": "application/ld+json",
                    "contentUrl": "/api/v1/source-b/current"
                },
                "measurementTechnique": "Water level sensor",
                "variableMeasured": {
                    "@type": "PropertyValue",
                    "name": "Water Level",
                    "unitCode": "MMT"
                },
                "spatialCoverage": {
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
                    }
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
        ],
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "dcterms:conformsTo": "https://www.w3.org/TR/shacl/"
    }


@router.get("/shapes/shacl")
async def get_shacl_shapes():
    """
    Get SHACL shapes for water level data validation
    
    Returns SHACL shapes that describe the expected structure
    and constraints for water level measurements.
    
    IMPORTANT for validation:
    The data from /source-a/current and /source-b/current includes a @context
    that maps property names to URIs (e.g., measuredAt → sosa:resultTime).
    Your SHACL validator must expand the JSON-LD to RDF before validation,
    ensuring that context-mapped properties are properly resolved to their
    full URIs. Most SHACL validators (pySHACL, Apache Jena, etc.) do this
    automatically when processing JSON-LD with @context.
    """
    return {
        "@context": {
            "sh": "http://www.w3.org/ns/shacl#",
            "schema": "https://schema.org/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "sosa": "http://www.w3.org/ns/sosa/",
            "dcterms": "http://purl.org/dc/terms/",
            "measuredAt": "sosa:resultTime",
            "conformsTo": "dcterms:conformsTo",
            "source": "https://schema.org/source"
        },
        "@graph": [
            {
                "@id": "urn:shapes:WaterLevelShape",
                "@type": "sh:NodeShape",
                "sh:targetClass": "schema:PropertyValue",
                "sh:property": [
                    {
                        "sh:path": "schema:name",
                        "sh:datatype": "xsd:string",
                        "sh:minCount": 1,
                        "sh:maxCount": 1,
                        "sh:pattern": "Water Level.*"
                    },
                    {
                        "sh:path": "schema:value",
                        "sh:datatype": "xsd:decimal",
                        "sh:minCount": 1,
                        "sh:maxCount": 1,
                        "sh:minInclusive": 0
                    },
                    {
                        "sh:path": "schema:unitCode",
                        "sh:datatype": "xsd:string",
                        "sh:minCount": 1,
                        "sh:maxCount": 1,
                        "sh:in": ["CMT", "MMT"],
                        "sh:message": "Unit code must be CMT (centimetre) or MMT (millimetre) from UN/CEFACT Common Code standard"
                    },
                    {
                        "sh:path": "sosa:resultTime",
                        "sh:datatype": "xsd:dateTime",
                        "sh:minCount": 1,
                        "sh:maxCount": 1
                    },
                    {
                        "sh:path": "schema:location",
                        "sh:minCount": 1,
                        "sh:maxCount": 1,
                        "sh:node": {
                            "@type": "sh:NodeShape",
                            "sh:property": [
                                {
                                    "sh:path": "schema:geo",
                                    "sh:minCount": 1,
                                    "sh:node": {
                                        "@type": "sh:NodeShape",
                                        "sh:property": [
                                            {
                                                "sh:path": "schema:latitude",
                                                "sh:datatype": "xsd:decimal",
                                                "sh:minCount": 1,
                                                "sh:maxCount": 1
                                            },
                                            {
                                                "sh:path": "schema:longitude",
                                                "sh:datatype": "xsd:decimal",
                                                "sh:minCount": 1,
                                                "sh:maxCount": 1
                                            }
                                        ]
                                    }
                                },
                                {
                                    "sh:path": "dcterms:conformsTo",
                                    "sh:minCount": 1,
                                    "sh:message": "Must declare conformance to standards (ISO TC 211 GMD, INSPIRE, ISO Hydrometry)",
                                    "sh:description": "Expected standards: ISO 19115-1, INSPIRE Regulation 1089/2010, INSPIRE Hydrography, ISO 748, ISO 1100"
                                }
                            ]
                        }
                    }
                ]
            },
            {
                "@id": "urn:shapes:SourceAShape",
                "@type": "sh:NodeShape",
                "sh:target": {
                    "@type": "sh:SPARQLTarget",
                    "sh:select": "SELECT ?this WHERE { ?this <https://schema.org/source> 'Source A' . }"
                },
                "sh:property": [
                    {
                        "sh:path": "schema:unitCode",
                        "sh:hasValue": "CMT",
                        "sh:message": "Source A must use centimeters (CMT)"
                    },
                    {
                        "sh:path": "schema:value",
                        "sh:minInclusive": 1300,
                        "sh:maxInclusive": 2200,
                        "sh:message": "Source A value must be between 1300 and 2200 cm"
                    }
                ]
            },
            {
                "@id": "urn:shapes:SourceBShape",
                "@type": "sh:NodeShape",
                "sh:target": {
                    "@type": "sh:SPARQLTarget",
                    "sh:select": "SELECT ?this WHERE { ?this <https://schema.org/source> 'Source B' . }"
                },
                "sh:property": [
                    {
                        "sh:path": "schema:unitCode",
                        "sh:hasValue": "MMT",
                        "sh:message": "Source B must use millimeters (MMT)"
                    },
                    {
                        "sh:path": "schema:value",
                        "sh:minInclusive": 13000,
                        "sh:maxInclusive": 22000,
                        "sh:message": "Source B value must be between 13000 and 22000 mm"
                    }
                ]
            }
        ]
    }


@router.get("/shapes/odrl")
async def get_odrl_policies():
    """
    Get ODRL policies for data usage
    
    Returns ODRL policies describing permitted uses of the water level data.
    This is an open data policy - everyone can freely use, share, and reuse this data.
    """
    return {
        "@context": "http://www.w3.org/ns/odrl/2/",
        "@type": "Set",
        "@id": "urn:policy:water-monitoring:open-access",
        "profile": "http://www.w3.org/ns/odrl/2/core",
        "permission": [
            {
                "target": ["urn:dataset:source-a", "urn:dataset:source-b", "urn:dataset:antwerp"],
                "action": [
                    "use",
                    "read",
                    "reproduce",
                    "distribute",
                    "derive",
                    "commercialize"
                ],
                "assignee": "http://www.w3.org/ns/odrl/2/Public"
            }
        ]
    }
