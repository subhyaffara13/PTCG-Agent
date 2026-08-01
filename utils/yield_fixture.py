
def yield_fixture(
    fixture_function=None,
    *args,
    scope="function",
    params=None,
    autouse=False,
    ids=None,
    name=None,
):
    """(Return a) decorator to mark a yield-fixture factory function.

    .. deprecated:: 3.0
        Use :py:func:`pytest.fixture` directly instead.
    """
    warnings.warn(YIELD_FIXTURE, stacklevel=2)
    return fixture(
        fixture_function,
        *args,
        scope=scope,
        params=params,
        autouse=autouse,
        ids=ids,
        name=name,
    )

