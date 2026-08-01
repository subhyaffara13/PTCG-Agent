
def _decode_oauth_payload(stored: str) -> Optional[Dict[str, Any]]:
    """Return the OAuth2 payload dict if ``stored`` holds one, else ``None``.

    A row is considered an OAuth2 credential iff its decoded value parses as
    a JSON object with ``"type": "oauth2"``.  Plain BYOK credentials (which
    share the same column) decode to a non-JSON string and return ``None``.
    """
    decoded = _decode_user_credential(stored)
    if decoded is None:
        return None
    try:
        parsed = json.loads(decoded)
    except (ValueError, TypeError):
        return None
    if isinstance(parsed, dict) and parsed.get("type") == "oauth2":
        return parsed
    return None

