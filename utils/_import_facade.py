
def _import_facade(attr: str) -> object:
    """Import the public API from the `api` module."""
    if attr in _PUBLIC_API:
        from . import api  # pylint: disable=import-outside-toplevel

        return getattr(api, attr)
    raise AttributeError(f"module '{__package__}' has no attribute '{attr}'")

