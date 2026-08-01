
def _get_credentials() -> Optional[str]:
    """Get GigaChat credentials from environment."""
    return get_secret_str("GIGACHAT_CREDENTIALS") or get_secret_str("GIGACHAT_API_KEY")

