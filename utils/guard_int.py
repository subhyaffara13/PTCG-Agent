
def guard_int(a: IntLikeType) -> int:
    if isinstance(a, SymInt):
        return a.node.guard_int("", 0)  # NB: uses Python backtrace
    if type(a) is not int:
        raise AssertionError(f"Expected int, got {a}")
    return a

