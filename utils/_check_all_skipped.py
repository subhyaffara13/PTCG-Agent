
def _check_all_skipped(test: doctest.DocTest) -> None:
    """Raise pytest.skip() if all examples in the given DocTest have the SKIP
    option set."""
    import doctest

    all_skipped = all(x.options.get(doctest.SKIP, False) for x in test.examples)
    if all_skipped:
        skip("all tests skipped by +SKIP option")

