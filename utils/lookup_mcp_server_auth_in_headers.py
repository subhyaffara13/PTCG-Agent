from typing import Dict, Optional, Union

def lookup_mcp_server_auth_in_headers(
    mcp_server_auth_headers: Mapping[str, Union[str, Dict[str, str]]],
    *,
    alias: Optional[str] = None,
    server_name: Optional[str] = None,
) -> Optional[Union[str, Dict[str, str]]]:
    """
    Resolve server-specific auth headers with case-insensitive matching.

    Tries the raw alias/server_name (lowercased) and the header-safe sanitized
    alias so dashboard clients using sanitize_mcp_alias_for_header() still match.
    """
    if not mcp_server_auth_headers:
        return None

    normalized_headers = {k.lower(): v for k, v in mcp_server_auth_headers.items()}

    for identifier in (alias, server_name):
        if not identifier:
            continue
        keys_to_try = [identifier.lower()]
        sanitized = sanitize_mcp_alias_for_header(identifier)
        if sanitized and sanitized not in keys_to_try:
            keys_to_try.append(sanitized)
        for key in keys_to_try:
            if key in normalized_headers:
                return normalized_headers[key]
    return None

