
def _get_dsl_registry():
    """Lazy import to avoid circular imports."""
    from torch._native.dsl_registry import dsl_registry

    return dsl_registry

