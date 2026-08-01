
def _is_pip_available() -> bool:
    """Return `True` if pip is importable in the current environment."""
    return importlib.util.find_spec("pip") is not None

