
def _has_auth_header(headers: Headers) -> bool:
    return _has_header(headers, "Authorization") or _has_header(headers, "api-key")

