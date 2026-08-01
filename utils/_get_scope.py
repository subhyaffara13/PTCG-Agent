
def _get_scope() -> str:
    """Get GigaChat scope from environment or use default."""
    return get_secret_str("GIGACHAT_SCOPE") or GIGACHAT_SCOPE

