
def freeze_includes() -> list[str]:
    """Return a list of module names used by pytest that should be
    included by cx_freeze."""
    import _pytest

    result = list(_iter_all_modules(_pytest))
    return result

