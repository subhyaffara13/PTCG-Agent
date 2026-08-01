
def assert_dict_equal(
    self_: Any, d1: dict[T, U], d2: dict[T, U], msg: str | None = None
) -> None:
    self_.assertTrue(d1 == d2, msg)


def assert_dict_equal(left, right, compare_keys: bool = True) -> None:
    _check_isinstance(left, right, dict)
    _testing.assert_dict_equal(left, right, compare_keys=compare_keys)

