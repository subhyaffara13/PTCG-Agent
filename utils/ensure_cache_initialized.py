
def ensure_cache_initialized() -> None:
    """Ensure the kernel cache is initialized."""
    global _kernel_by_name_cache

    if _kernel_by_name_cache is None:
        _kernel_by_name_cache = _build_kernel_cache()

