
def _get_first_non_fixture_func(obj: object, names: Iterable[str]) -> object | None:
    """Return the attribute from the given object to be used as a setup/teardown
    xunit-style function, but only if not marked as a fixture to avoid calling it twice.
    """
    for name in names:
        meth: object | None = getattr(obj, name, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            return meth
    return None

