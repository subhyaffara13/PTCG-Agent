
def _caller_key(user_api_key_dict: UserAPIKeyAuth) -> Optional[str]:
    """Return the hashed key token that identifies this caller, or None for master key."""
    return user_api_key_dict.token

