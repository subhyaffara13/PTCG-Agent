
def json_parse(text: str) -> Optional[Any]:
    """
    Parse a JSON string into a Python object.

    Args:
        text: The JSON string to parse

    Returns:
        Parsed Python object, or None if parsing fails
    """
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError) as e:
        verbose_proxy_logger.debug(f"Starlark json_parse error: {e}")
        return None

