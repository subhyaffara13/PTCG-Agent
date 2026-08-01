
def _get_fixtures_per_test(test: nodes.Item) -> Iterator[FixtureDef[object]]:
    """Returns all fixtures used by the test item except for those created by
    direct parametrization and those requested dynamically with
    ``request.getfixturevalue``.

    The justification for excluding fixtures created by direct parametrization
    is that for users, they are internal implementation detail.

    Dynamically requested fixtures are excluded because they are not known
    statically.
    """
    from _pytest.python import DirectParamFixtureDef

    # Custom Items may not have _fixtureinfo attribute.
    fixture_info: FuncFixtureInfo | None = getattr(test, "_fixtureinfo", None)
    if fixture_info is None:
        return  # pragma: no cover

    # dict key not used in loop but needed for sorting.
    for argname, fixturedefs in sorted(fixture_info.name2fixturedefs.items()):
        if not fixturedefs:
            # Not supposed to be empty, but for safety.
            continue  # pragma: no cover
        # Last item is expected to be the one directly used by the test item.
        fixturedef = fixturedefs[-1]
        if isinstance(fixturedef, DirectParamFixtureDef):
            continue
        yield fixturedef

