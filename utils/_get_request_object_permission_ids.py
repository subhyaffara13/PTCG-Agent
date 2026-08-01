
def _get_request_object_permission_ids(
    request_data: dict,
) -> Tuple[Optional[str], Optional[str]]:
    """Extract object_permission_id and team_object_permission_id from request_data."""
    if not request_data:
        return None, None
    for key in ("litellm_metadata", "metadata"):
        meta = request_data.get(key)
        if not isinstance(meta, dict):
            continue
        auth = meta.get("user_api_key_auth")
        if auth is not None and hasattr(auth, "object_permission_id"):
            key_op = getattr(auth, "object_permission_id", None)
            team_op = getattr(auth, "team_object_permission_id", None)
            if key_op is not None or team_op is not None:
                return (
                    str(key_op).strip() if key_op else None,
                    str(team_op).strip() if team_op else None,
                )
        key_op = meta.get("user_api_key_object_permission_id")
        team_op = meta.get("user_api_key_team_object_permission_id")
        if key_op is not None or team_op is not None:
            return (
                str(key_op).strip() if key_op else None,
                str(team_op).strip() if team_op else None,
            )
    return None, None

