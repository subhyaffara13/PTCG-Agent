
def _get_client_init_params(cls: type) -> Tuple[str, ...]:
    """Extract __init__ parameter names (excluding 'self') from a class."""
    return tuple(p for p in inspect.signature(cls.__init__).parameters if p != "self")  # type: ignore[misc]

