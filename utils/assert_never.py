
def assert_never(x: NoReturn) -> NoReturn:  # pragma: no cover
    """
    A hint to the typechecker that a branch can never occur.
    """
    raise AssertionError(f"unhandled type: {type(x).__name__}")


def assert_never(obj: NoReturn, msg: str) -> NoReturn:
    """
    Helper to make sure that we have covered all possible types.

    This is mostly useful for ``mypy``, docs:
    https://mypy.readthedocs.io/en/latest/literal_types.html#exhaustive-checks
    """
    raise TypeError(msg)

