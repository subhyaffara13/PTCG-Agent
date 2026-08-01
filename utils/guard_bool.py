
def guard_bool(a: BoolLikeType) -> bool:
    if isinstance(a, SymBool):
        return a.node.guard_bool("", 0)  # NB: uses Python backtrace
    if type(a) is not bool:
        raise AssertionError(f"Expected bool, got {a}")
    return a

