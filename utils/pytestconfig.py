
def pytestconfig(request: FixtureRequest) -> Config:
    """Session-scoped fixture that returns the session's :class:`pytest.Config`
    object.

    Example::

        def test_foo(pytestconfig):
            if pytestconfig.get_verbosity() > 0:
                ...

    """
    return request.config

