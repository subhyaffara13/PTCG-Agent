
def _exclude_efc_kernels(metadata) -> bool:
    """
    Filter out EFC kernels.

    EFC kernels support custom epilogue operations but have additional overhead.
    Since NVGEMM doesn't support epilogue fusion yet (see nv_universal_gemm_scheduling.py),
    we use non-EFC kernels which are equivalent for identity epilogue (out = acc).
    TODO(nikhilap): Remove this filter once NVGEMM supports epilogue fusion.
    """
    return "EFC" not in metadata.kernel_class.__name__

