
def json_stringify(obj: Any) -> str:
    """
    Convert a Python object to a JSON string.

    Args:
        obj: The object to serialize

    Returns:
        JSON string representation
    """
    try:
        return json.dumps(obj)
    except (TypeError, ValueError) as e:
        verbose_proxy_logger.warning(f"Starlark json_stringify error: {e}")
        return ""

