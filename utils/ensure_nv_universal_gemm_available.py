
def ensure_nv_universal_gemm_available() -> bool:
    """Check if NVIDIA Universal GEMM (cutlass_api) is importable; cache the result for reuse.

    Call ensure_nv_universal_gemm_available.cache_clear() after installing cutlass_api
    in the same interpreter to retry the import.
    """
    try:
        available = importlib.util.find_spec("cutlass_api") is not None
    except ImportError:
        return False
    if available:
        _ensure_fp4_dtype_registered()
    return available

