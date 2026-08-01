
def has_backend(backend: str) -> bool:
    """Checks if the backend is known."""
    return backend.lower() in CONVERT_BACKENDS

