
def assert_eq(a: _T, b: _T) -> None:
    if a != b:
        raise AssertionError(f"{a} != {b}")

