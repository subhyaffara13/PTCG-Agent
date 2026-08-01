
def _parse_config_value(raw: Any) -> Dict[str, Any]:
    """Parse a config_value from DB (may be JSON string or dict)."""
    if isinstance(raw, str):
        return safe_json_loads(raw, default={})
    return dict(raw)

