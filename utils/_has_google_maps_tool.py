from typing import Any, Optional

def _has_google_maps_tool(tools: Optional[Any]) -> bool:
    """Return True if any tool object in the list has a 'googleMaps' key."""
    if not isinstance(tools, list):
        return False
    return any(
        isinstance(t, dict) and VertexToolName.GOOGLE_MAPS.value in t for t in tools
    )

