
def _get_field(result: Any, key: str, default: Any = None) -> Any:
    """Read a field from either a dict/TypedDict or an attribute-based object."""
    if isinstance(result, dict):
        return result.get(key, default)
    return getattr(result, key, default)

