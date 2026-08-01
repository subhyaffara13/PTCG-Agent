
def _parse_rich_type_value(value: Any) -> str:
    """Parse rich (toml) types into strings."""
    if isinstance(value, (list, tuple)):
        return ",".join(_parse_rich_type_value(i) for i in value)
    if isinstance(value, re.Pattern):
        return str(value.pattern)
    if isinstance(value, dict):
        return ",".join(f"{k}:{v}" for k, v in value.items())
    return str(value)

