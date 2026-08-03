from typing import Optional

def get_user_id_from_request(request: Request) -> Optional[str]:
    """
    Get the user id from the request
    """
    # Get the raw query string and parse it properly to handle + characters
    user_id: Optional[str] = None
    query_string = str(request.url.query)
    if "user_id=" in query_string:
        # Extract the user_id value from the raw query string
        import re
        from urllib.parse import unquote

        match = re.search(r"user_id=([^&]*)", query_string)
        if match:
            # Use unquote instead of unquote_plus to preserve + characters
            raw_user_id = unquote(match.group(1))
            if _is_valid_user_id(raw_user_id):
                user_id = raw_user_id
    return user_id

