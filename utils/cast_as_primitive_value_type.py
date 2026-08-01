
def cast_as_primitive_value_type(value) -> Union[str, bool, int, float]:
    """
    Converts a value to an OTEL-supported primitive for Arize/Phoenix observability.
    """
    if value is None:
        return ""
    if isinstance(value, (str, bool, int, float)):
        return value
    try:
        return str(value)
    except Exception:
        return ""

