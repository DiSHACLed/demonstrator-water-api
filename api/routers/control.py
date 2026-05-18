from fastapi import APIRouter, HTTPException
from api.models import WaterLevelControl, ActiveSourceControl
from api.routers import sources

router = APIRouter()


@router.post("/set-level")
async def set_water_level(control: WaterLevelControl):
    """
    Set the water level for demonstration purposes
    
    This endpoint allows the control center to adjust water levels
    """
    sources.current_water_level["percentage"] = control.level_percentage
    
    # Force immediate recalculation by resetting the timestamp
    # This ensures both sources get synchronized with the new value right away
    sources._base_level_cache["last_update"] = 0
    
    return {
        "@context": "https://schema.org/",
        "@type": "Action",
        "actionStatus": "CompletedActionStatus",
        "name": "Set Water Level",
        "result": {
            "@type": "PropertyValue",
            "name": "Water Level Control",
            "value": control.level_percentage,
            "unitCode": "P1",  # Percentage
            "description": f"Water level set to {control.level_percentage}%"
        }
    }


@router.get("/current-settings")
async def get_current_settings():
    """
    Get current control settings
    
    Returns the current water level percentage
    """
    return {
        "@context": "https://schema.org/",
        "@type": "PropertyValue",
        "name": "Control Settings",
        "value": sources.current_water_level["percentage"],
        "unitCode": "P1"
    }


@router.post("/set-active-source")
async def set_active_source(control: ActiveSourceControl):
    """
    Set which source is active/primary for the Antwerp endpoint
    
    Args:
        control: Object containing source_name ("source-a" or "source-b")
    """
    if control.source_name not in ["source-a", "source-b"]:
        raise HTTPException(
            status_code=400, 
            detail="Invalid source name. Must be 'source-a' or 'source-b'"
        )
    
    sources.active_source["name"] = control.source_name
    
    return {
        "@context": "https://schema.org/",
        "@type": "Action",
        "actionStatus": "CompletedActionStatus",
        "name": "Set Active Source",
        "result": {
            "@type": "PropertyValue",
            "name": "Active Water Source",
            "value": control.source_name,
            "description": f"Active source set to {control.source_name}"
        }
    }


@router.get("/active-source")
async def get_active_source():
    """
    Get the currently active water source
    
    Returns which source (A or B) is currently marked as primary
    """
    return {
        "@context": "https://schema.org/",
        "@type": "PropertyValue",
        "name": "Active Water Source",
        "value": sources.active_source["name"]
    }
