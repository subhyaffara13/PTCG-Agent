
def ensure_nvmatmul_heuristics_available() -> bool:
    """Check if nvMatmulHeuristics is importable; cache the result for reuse.

    nvMatmulHeuristics provides performance model-based kernel selection
    for NVIDIA GEMM operations.

    Call ensure_nvmatmul_heuristics_available.cache_clear() after installing
    nvMatmulHeuristics in the same interpreter to retry the import.
    """
    try:
        return importlib.util.find_spec("nvMatmulHeuristics") is not None
    except ImportError:
        return False

