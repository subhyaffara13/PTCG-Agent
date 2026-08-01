
def _p_value(observed: int, dist: list[int]) -> float:
    """P(permuted >= observed). One-sided; Σ|Δrank| can only be positive."""
    if not dist:
        return float("nan")
    return sum(1 for x in dist if x >= observed) / len(dist)

