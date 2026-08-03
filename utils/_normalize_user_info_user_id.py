from typing import Optional

def _normalize_user_info_user_id(
    request: Request, user_id: Optional[str]
) -> Optional[str]:
    """Normalize URL-decoded user_id while preserving '+' characters."""
    if user_id is not None and " " in user_id:
        return get_user_id_from_request(request=request)
    return user_id

