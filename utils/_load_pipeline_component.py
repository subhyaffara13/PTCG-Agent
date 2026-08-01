
def _load_pipeline_component(load_flag, component, loader):
    """Load an optional pipeline component, preserving the original soft-failure behavior."""
    if not (load_flag or load_flag is None):
        return component

    try:
        return loader(component)
    except Exception:
        if load_flag:
            raise
        return None

