
def has_numpy() -> bool:
    try:
        import numpy  # noqa: F401  # pyright: ignore[reportUnusedImport]
    except ImportError:
        return False

    return True

