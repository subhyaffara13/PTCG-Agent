
def guard_float(a: FloatLikeType) -> float:
    if isinstance(a, SymFloat):
        return a.node.guard_float("", 0)  # NB: uses Python backtrace
    if not isinstance(a, float):
        raise AssertionError(f"Expected float, got {a}")
    return a

