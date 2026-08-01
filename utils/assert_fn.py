
def assert_fn(x: object) -> None:
    if not x:
        raise AssertionError("Assertion failed")

