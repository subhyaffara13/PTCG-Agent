
def get_compatible_kernels(
    args: Any,
    cc: int,
    metadata_filter: Callable[[Any], bool] | None = None,
) -> list[Any]:
    """Get kernels compatible with the given arguments from the cache."""
    global _kernel_by_name_cache

    if _kernel_by_name_cache is None:
        _kernel_by_name_cache = _build_kernel_cache()

    compatible = []
    for kernel in _kernel_by_name_cache.values():
        if kernel.metadata.min_cc > cc:
            continue

        if metadata_filter is not None and not metadata_filter(kernel.metadata):
            continue

        status = kernel.supports(args)
        if status.error is not None:
            continue
        compatible.append(kernel)

    log.debug(
        "Found %d compatible kernels from cache of %d total",
        len(compatible),
        len(_kernel_by_name_cache),
    )
    return compatible

