
def expect_true(a: BoolLikeType, skip: int = 0) -> bool:
    if isinstance(a, SymBool):
        # TODO: check perf implications of this
        frame = inspect.currentframe()
        for _ in range(skip + 1):  # always run this loop at least once
            if frame is None:
                break
            frame = frame.f_back
        return a.node.expect_true(
            frame.f_code.co_filename if frame else "", frame.f_lineno if frame else 0
        )
    if type(a) is not bool:
        raise AssertionError(f"Expected bool, got {a}")
    return a

