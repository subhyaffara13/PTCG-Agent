
def get_kernel_by_name(kernel_name: str) -> Any:
    """Get a cutlass_api kernel by name using the global cache."""
    global _kernel_by_name_cache

    if _kernel_by_name_cache is None:
        _kernel_by_name_cache = _build_kernel_cache()

    return _kernel_by_name_cache.get(kernel_name)

