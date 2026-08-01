
def get_nvgemm_heuristics() -> NVUniversalGemmHeuristics:
    """Get the singleton NVUniversalGemmHeuristics instance."""
    global _nvgemm_heuristics
    if _nvgemm_heuristics is None:
        _nvgemm_heuristics = NVUniversalGemmHeuristics()
    return _nvgemm_heuristics

