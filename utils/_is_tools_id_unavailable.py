
def _is_tools_id_unavailable() -> bool:
    """Return True if we already know cudaGraphNodeGetToolsId is missing."""
    if not _HAS_CUDA_BINDINGS:
        return True
    if _tools_id_available is False:
        return True
    if not hasattr(_cuda_runtime, "cudaGraphNodeGetToolsId"):
        return True
    return False

