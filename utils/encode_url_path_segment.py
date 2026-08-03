from typing import Any

def encode_url_path_segment(value: Any, *, field_name: str = "path parameter") -> str:
    """Percent-encode one user-controlled URL path segment.

    ``urllib.parse.quote(..., safe="")`` intentionally leaves RFC 3986
    unreserved characters such as ``.`` unescaped, so reject standalone dot
    segments before they can be appended to an upstream URL and normalized by
    the HTTP client.
    """
    if value is None:
        raise ValueError(f"{field_name} is required")

    value_str = str(value)
    if value_str == "":
        raise ValueError(f"{field_name} is required")
    if value_str in {".", ".."}:
        raise ValueError(f"{field_name} cannot be a dot path segment")

    return quote(value_str, safe="")

