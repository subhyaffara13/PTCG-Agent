
def _compute_mm_arithmetic_intensity(M: int, N: int, K: int) -> float:
    return M * N * K / (M * K + N * K + M * N)

