"""V2 measurement endpoints.

These endpoints behave exactly like their V1 counterparts in ``sources.py``:
they read from the same shared control state (water level slider and active
source) and therefore react to the same buttons, toggles and control calls.

The only difference is the response representation. Instead of the schema.org
``PropertyValue`` shape used by V1, V2 advertises each reading as JSON-LD using
the SOSA / QUDT vocabularies, mirroring the Turtle structure used by the
DiSHACLed demonstrator (sosa:Observation -> sosa:hasResult -> qudt:QuantityValue).
"""

from fastapi import APIRouter, Request
from fastapi.responses import Response
from datetime import datetime, timezone

# Reuse the shared state and base-level logic from the V1 module so that both
# API versions stay perfectly synchronized and react to the same controls.
from api.routers import sources

router = APIRouter()

# JSON-LD context matching the demonstrator sample (SOSA + QUDT).
V2_CONTEXT = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "ex": "http://www.example.org/",
    "schema": "http://schema.org/",
    "sosa": "http://www.w3.org/ns/sosa/",
    "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#",
    "qudt": "http://qudt.org/schema/qudt/",
    "unit": "http://qudt.org/vocab/unit/",
    "dcterms": "http://purl.org/dc/terms/",
}

# QUDT unit IRIs for the units used by each source.
QUDT_UNIT_CENTIMETRE = "unit:CentiM"
QUDT_UNIT_MILLIMETRE = "unit:MilliM"


def _build_observation(
    source_key: str,
    sensor_id: str,
    value: float,
    qudt_unit: str,
    sensor_brand: str,
) -> dict:
    """Build a single SOSA Observation as a JSON-LD document.

    Args:
        source_key: Short identifier for the source (e.g. ``source-a``), used to
            build stable-looking node identifiers.
        sensor_id: The ``ex:`` sensor node that made the observation.
        value: The measured numeric value.
        qudt_unit: The QUDT unit IRI (e.g. ``unit:CentiM``).
        sensor_brand: The brand name of the sensor.
    """
    timestamp = datetime.now(timezone.utc)
    ts_iso = timestamp.strftime("%Y-%m-%dT%H:%M:%S")

    obs_id = f"ex:obs-{source_key}-{ts_iso}"
    qty_id = f"ex:qty-{source_key}-{ts_iso}"

    return {
        "@context": V2_CONTEXT,
        "@id": obs_id,
        "@type": "sosa:Observation",
        "sosa:madeBySensor": {"@id": sensor_id, "SensorBrand": sensor_brand},
        "sosa:resultTime": {
            "@value": ts_iso,
            "@type": "xsd:dateTime",
        },
        "sosa:hasResult": {
            "@id": qty_id,
            "@type": "qudt:QuantityValue",
            "qudt:numericValue": {
                "@value": str(round(value, 2)),
                "@type": "xsd:decimal",
            },
            "qudt:unit": {"@id": qudt_unit},
        },
    }


_SOURCE_A_EXAMPLE = {
    "@context": V2_CONTEXT,
    "@id": "ex:obs-source-a-2026-03-25T10:30:00",
    "@type": "sosa:Observation",
    "sosa:madeBySensor": {"@id": "ex:sensor-a", "SensorBrand": "HydroMeasureX5"},
    "sosa:resultTime": {"@value": "2026-03-25T10:30:00", "@type": "xsd:dateTime"},
    "sosa:hasResult": {
        "@id": "ex:qty-source-a-2026-03-25T10:30:00",
        "@type": "qudt:QuantityValue",
        "qudt:numericValue": {"@value": "1750.5", "@type": "xsd:decimal"},
        "qudt:unit": {"@id": QUDT_UNIT_CENTIMETRE},
    },
}

_SOURCE_B_EXAMPLE = {
    "@context": V2_CONTEXT,
    "@id": "ex:obs-source-b-2026-03-25T14:30:00",
    "@type": "sosa:Observation",
    "sosa:madeBySensor": {"@id": "ex:sensor-b", "SensorBrand": "WaterProber3"},
    "sosa:resultTime": {"@value": "2026-03-25T14:30:00", "@type": "xsd:dateTime"},
    "sosa:hasResult": {
        "@id": "ex:qty-source-b-2026-03-25T14:30:00",
        "@type": "qudt:QuantityValue",
        "qudt:numericValue": {"@value": "17505.0", "@type": "xsd:decimal"},
        "qudt:unit": {"@id": QUDT_UNIT_MILLIMETRE},
    },
    "waterTemperature": "18°C",
}


def _source_a_observation() -> dict:
    """Build the Source A SOSA/QUDT observation dict (centimetres)."""
    base_level = sources.get_base_level()
    # Convert percentage to cm (13-22 meters) - identical to V1.
    value_cm = 1300 + (base_level * 9.0)
    return _build_observation(
        source_key="source-a",
        sensor_id="ex:sensor-a",
        value=value_cm,
        qudt_unit=QUDT_UNIT_CENTIMETRE,
        sensor_brand="HydroMeasureX5",
    )


def _source_b_observation() -> dict:
    """Build the Source B SOSA/QUDT observation dict (millimetres)."""
    base_level = sources.get_base_level()
    # Convert percentage to mm (13-22 meters) - identical to V1.
    value_mm = 13000 + (base_level * 90.0)
    observation = _build_observation(
        source_key="source-b",
        sensor_id="ex:sensor-b",
        value=value_mm,
        qudt_unit=QUDT_UNIT_MILLIMETRE,
        sensor_brand="WaterProber3",
    )
    # Source B additionally reports water temperature (Source A does not).
    observation["waterTemperature"] = "18°C"
    return observation


@router.api_route(
    "/source-a/current",
    methods=["GET", "HEAD"],
    summary="Source A current level (SOSA/QUDT JSON-LD)",
    response_description="A sosa:Observation whose result is a qudt:QuantityValue in centimetres (unit:CentiM).",
    description=(
        "Returns the current water level from **Source A** as a single "
        "`sosa:Observation` in JSON-LD, using the SOSA and QUDT vocabularies.\n\n"
        "This is the V2 representation of `GET /api/v1/source-a/current`. It reads "
        "the **same shared control state** (water-level slider and 5s cached base "
        "value), so it reacts to the same control calls and stays synchronized with "
        "the V1 and Source B endpoints.\n\n"
        "- **Value unit:** centimetres (`unit:CentiM`)\n"
        "- **Value formula:** `1300 + base_level * 9.0`\n"
        "- **Result shape:** `sosa:Observation` \u2192 `sosa:hasResult` \u2192 `qudt:QuantityValue`"
    ),
    responses={
        200: {
            "description": (
                "Current water level from Source A as a SOSA Observation in "
                "JSON-LD. Value is in centimetres (QUDT unit:CentiM)."
            ),
            "content": {
                "application/ld+json": {"example": _SOURCE_A_EXAMPLE},
                "application/json": {"example": _SOURCE_A_EXAMPLE},
            },
        }
    },
)
async def get_source_a_current_v2(request: Request):
    """Get current water level from Source A (centimetres) as SOSA/QUDT JSON-LD."""
    return sources._negotiate_measurement_response(request, _source_a_observation())


@router.api_route(
    "/source-b/current",
    methods=["GET", "HEAD"],
    summary="Source B current level (SOSA/QUDT JSON-LD)",
    response_description="A sosa:Observation whose result is a qudt:QuantityValue in millimetres (unit:MilliM).",
    description=(
        "Returns the current water level from **Source B** as a single "
        "`sosa:Observation` in JSON-LD, using the SOSA and QUDT vocabularies.\n\n"
        "This is the V2 representation of `GET /api/v1/source-b/current`. It reads "
        "the **same shared control state** (water-level slider and 5s cached base "
        "value), so it reacts to the same control calls and stays synchronized with "
        "the V1 and Source A endpoints.\n\n"
        "- **Value unit:** millimetres (`unit:MilliM`)\n"
        "- **Value formula:** `13000 + base_level * 90.0`\n"
        "- **Result shape:** `sosa:Observation` \u2192 `sosa:hasResult` \u2192 `qudt:QuantityValue`"
    ),
    responses={
        200: {
            "description": (
                "Current water level from Source B as a SOSA Observation in "
                "JSON-LD. Value is in millimetres (QUDT unit:MilliM)."
            ),
            "content": {
                "application/ld+json": {"example": _SOURCE_B_EXAMPLE},
                "application/json": {"example": _SOURCE_B_EXAMPLE},
            },
        }
    },
)
async def get_source_b_current_v2(request: Request):
    """Get current water level from Source B (millimetres) as SOSA/QUDT JSON-LD."""
    return sources._negotiate_measurement_response(request, _source_b_observation())


@router.api_route(
    "/antwerp/current",
    methods=["GET", "HEAD"],
    summary="Antwerp current level (active source, SOSA/QUDT JSON-LD)",
    response_description="A sosa:Observation from whichever source is currently active (A or B).",
    description=(
        "Returns the current water level for **Antwerp** as a single "
        "`sosa:Observation` in JSON-LD. This endpoint is a proxy that delegates to "
        "either Source A or Source B based on the shared **active-source** setting, "
        "so it reacts to the same source toggle as the V1 endpoint.\n\n"
        "The unit therefore follows the active source: centimetres (`unit:CentiM`) "
        "for Source A or millimetres (`unit:MilliM`) for Source B."
    ),
    responses={
        200: {
            "description": (
                "Current water level from Antwerp (proxy to active source) as a "
                "SOSA Observation in JSON-LD."
            ),
            "content": {
                "application/ld+json": {"example": _SOURCE_A_EXAMPLE},
                "application/json": {"example": _SOURCE_A_EXAMPLE},
            },
        }
    },
)
async def get_antwerp_current_v2(request: Request):
    """Get current water level from Antwerp (proxy to the active source).

    Delegates to either Source A or Source B based on the shared active-source
    setting, so it reacts to the same toggle as the V1 endpoint. Served as
    ``application/ld+json`` (content-negotiable).
    """
    if sources.active_source["name"] == "source-a":
        data = _source_a_observation()
    else:
        data = _source_b_observation()
    return sources._negotiate_measurement_response(request, data)
