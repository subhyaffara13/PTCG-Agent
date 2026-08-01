
def resolve_fixture_function(
    fixturedef: FixtureDef[FixtureValue], request: FixtureRequest
) -> _FixtureFunc[FixtureValue]:
    """Get the actual callable that can be called to obtain the fixture
    value."""
    fixturefunc = fixturedef.func
    # The fixture function needs to be bound to the actual
    # request.instance so that code working with "fixturedef" behaves
    # as expected.
    instance = request.instance

    if fixturedef._scope is Scope.Class:
        # Check if fixture is an instance method (bound to instance, not class)
        if hasattr(fixturefunc, "__self__"):
            bound_to = fixturefunc.__self__
            # classmethod: bound_to is the class itself (a type)
            # instance method: bound_to is an instance (not a type)
            if not isinstance(bound_to, type):
                warnings.warn(CLASS_FIXTURE_INSTANCE_METHOD, stacklevel=2)

    if instance is not None:
        # Handle the case where fixture is defined not in a test class, but some other class
        # (for example a plugin class with a fixture), see #2270.
        if hasattr(fixturefunc, "__self__") and not isinstance(
            instance,
            fixturefunc.__self__.__class__,
        ):
            return fixturefunc
        fixturefunc = getimfunc(fixturedef.func)
        if fixturefunc != fixturedef.func:
            fixturefunc = fixturefunc.__get__(instance)
    return fixturefunc

