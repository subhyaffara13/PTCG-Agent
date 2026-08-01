
def _filter_capabilities(upstream_capabilities: Any) -> Dict[str, Any]:
    """Return a capabilities dict containing only allowlisted, truthy keys."""
    if not isinstance(upstream_capabilities, dict):
        return {}
    return {
        key: value
        for key, value in upstream_capabilities.items()
        if key in _ALLOWED_CAPABILITY_KEYS and bool(value)
    }

