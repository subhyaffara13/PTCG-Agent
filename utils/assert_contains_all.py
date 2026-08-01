
def assert_contains_all(iterable, dic) -> None:
    for k in iterable:
        assert k in dic, f"Did not contain item: {k!r}"

