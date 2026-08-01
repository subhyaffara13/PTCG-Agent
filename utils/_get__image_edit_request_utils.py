
def _get_ImageEditRequestUtils() -> "ImageEditRequestUtils":
    """Get ImageEditRequestUtils, loading it lazily if needed."""
    global _ImageEditRequestUtils_cache
    if _ImageEditRequestUtils_cache is None:
        # Access via module to trigger __getattr__ if not cached
        module = importlib.import_module(__name__)
        _ImageEditRequestUtils_cache = module.ImageEditRequestUtils
    assert _ImageEditRequestUtils_cache is not None  # Type narrowing for type checker
    return _ImageEditRequestUtils_cache

