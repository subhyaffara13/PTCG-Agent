
def _teardown_yield_fixture(fixturefunc, it) -> None:
    """Execute the teardown of a fixture function by advancing the iterator
    after the yield and ensure the iteration ends (if not it means there is
    more than one yield in the function)."""
    try:
        next(it)
    except StopIteration:
        pass
    else:
        fs, lineno = getfslineno(fixturefunc)
        fail(
            f"fixture function has more than one 'yield':\n\n"
            f"{Source(fixturefunc).indent()}\n"
            f"{fs}:{lineno + 1}",
            pytrace=False,
        )

