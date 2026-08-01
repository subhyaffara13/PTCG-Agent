
def _handle_displayname_update(
    op_type: str, value: Any, update_data: Dict[str, Any]
) -> None:
    """Handle displayname updates."""
    if op_type == "remove":
        update_data["user_alias"] = None
    else:
        update_data["user_alias"] = str(value)

