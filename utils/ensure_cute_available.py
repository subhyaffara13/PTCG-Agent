
def ensure_cute_available() -> bool:
    """Check if CuTeDSL is importable; cache the result for reuse.

    Call ensure_cute_available.cache_clear() after installing CuTeDSL
    in the same interpreter to retry the import.
    """
    try:
        return importlib.util.find_spec("cutlass") is not None
    except ImportError:
        return False

