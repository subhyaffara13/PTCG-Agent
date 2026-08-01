
def _handle_name_update(
    path: str, op_type: str, value: Any, scim_metadata: Dict[str, Any]
) -> None:
    """Handle name field updates (givenName, familyName)."""
    if path == "name.givenname":
        if op_type == "remove":
            scim_metadata.pop("givenName", None)
        else:
            scim_metadata["givenName"] = str(value)
    elif path == "name.familyname":
        if op_type == "remove":
            scim_metadata.pop("familyName", None)
        else:
            scim_metadata["familyName"] = str(value)

