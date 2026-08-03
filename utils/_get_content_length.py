from typing import Optional

def _get_content_length(scope: Scope) -> Optional[int]:
    headers = dict(scope.get("headers") or [])
    raw_content_length = headers.get(b"content-length")
    if raw_content_length is None:
        return None

    try:
        return int(raw_content_length)
    except ValueError:
        return None

