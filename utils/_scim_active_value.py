from typing import Any, Dict, Optional

def _scim_active_value(metadata: Optional[Dict[str, Any]]) -> Optional[bool]:
    """Read the SCIM active flag from a user's metadata dict, if present."""
    if not metadata:
        return None
    value = metadata.get("scim_active")
    if value is None:
        return None
    return bool(value)

