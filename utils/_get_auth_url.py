
def _get_auth_url() -> str:
    """Get GigaChat auth URL from environment or use default."""
    return get_secret_str("GIGACHAT_AUTH_URL") or GIGACHAT_AUTH_URL

