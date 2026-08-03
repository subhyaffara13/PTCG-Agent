from typing import Any, Dict

def _handle_active_update(op_type: str, value: Any, metadata: Dict[str, Any]) -> None:
    """Handle active status updates."""
    if op_type == "remove":
        metadata.pop("scim_active", None)
    else:
        bool_val = value
        if isinstance(value, str):
            bool_val = value.lower() == "true"
        else:
            bool_val = bool(value)
        metadata["scim_active"] = bool_val

