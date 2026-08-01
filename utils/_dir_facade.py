
def _dir_facade() -> list[str]:
    """Include the public API in the module's dir() output."""
    return [*_PUBLIC_API, *globals().keys()]

