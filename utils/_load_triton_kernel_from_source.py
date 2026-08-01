
def _load_triton_kernel_from_source(
    kernel_name: str, source_code: str
) -> CachingAutotuner:
    return getattr(PyCodeCache.load(source_code), kernel_name)

