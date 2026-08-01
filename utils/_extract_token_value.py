
def _extract_token_value(token_value: Union[None, str, Dict[str, Any]]) -> str:
    """
    Extract token string from various formats (string, dict, etc.)

    Args:
        token_value: Token value in various formats (None, str, or dict with 'content' key)

    Returns:
        Extracted token string
    """
    if token_value is None or isinstance(token_value, str):
        return token_value or ""
    if isinstance(token_value, dict):
        return token_value.get("content", "")
    return ""

