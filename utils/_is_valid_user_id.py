
def _is_valid_user_id(user_id: str) -> bool:
    """Validate that a decoded user_id is safe to use downstream."""
    MAX_USER_ID_LENGTH = 512
    if len(user_id) > MAX_USER_ID_LENGTH:
        return False
    # Reject ASCII control characters (U+0000–U+001F)
    for ch in user_id:
        if ord(ch) < 0x20:
            return False
    return True

