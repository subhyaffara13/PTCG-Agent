
def _assert_is_none(value: object, msg: str) -> None:
    if value is not None:
        raise AssertionError(msg)

