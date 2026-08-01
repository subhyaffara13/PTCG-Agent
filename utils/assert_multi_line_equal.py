
def assert_multi_line_equal(
    self_: Any, first: T, second: T, msg: str | None = None
) -> None:
    return self_.assertTrue(first == second, msg)

