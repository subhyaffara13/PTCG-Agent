
def get_primary_resource_owner_scope(
    user_api_key_dict: Optional[UserAPIKeyAuth],
) -> Optional[str]:
    """Return the canonical owner scope to stamp on newly-created rows.

    ``None`` for identity-less callers — callers that depend on a primary
    scope to record ownership must surface that as a hard error rather
    than fall back to a shared sentinel (which would collapse every
    identity-less caller into the same logical owner).
    """
    if user_api_key_dict is None:
        return None

    if user_api_key_dict.user_id:
        return user_api_key_dict.user_id
    if user_api_key_dict.team_id:
        return f"team:{user_api_key_dict.team_id}"
    if user_api_key_dict.org_id:
        return f"org:{user_api_key_dict.org_id}"
    if user_api_key_dict.api_key:
        return f"key:{user_api_key_dict.api_key}"
    if user_api_key_dict.token:
        return f"key:{user_api_key_dict.token}"
    return None

