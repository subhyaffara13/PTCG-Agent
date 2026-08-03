from typing import Any, Dict

def _handle_externalid_update(
    op_type: str, value: Any, update_data: Dict[str, Any]
) -> None:
    """Handle externalid updates."""
    if op_type == "remove":
        update_data["sso_user_id"] = None
    else:
        update_data["sso_user_id"] = str(value)

