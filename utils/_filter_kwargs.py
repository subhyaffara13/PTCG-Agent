
def _filter_kwargs(kwargs: dict, cls: Type) -> dict:
    """Filter kwargs to only include parameters accepted by the class's __init__."""
    allowed = _get_init_params(cls)
    return {k: v for k, v in kwargs.items() if k in allowed}

