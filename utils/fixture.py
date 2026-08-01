
def fixture(
    fixture_function: Callable[..., object],
    *,
    scope: ScopeName | Callable[[str, Config], ScopeName] = ...,
    params: Iterable[object] | None = ...,
    autouse: bool = ...,
    ids: Sequence[object | None] | Callable[[Any], object | None] | None = ...,
    name: str | None = ...,
) -> FixtureFunctionDefinition: ...


def fixture(
    fixture_function: None = ...,
    *,
    scope: ScopeName | Callable[[str, Config], ScopeName] = ...,
    params: Iterable[object] | None = ...,
    autouse: bool = ...,
    ids: Sequence[object | None] | Callable[[Any], object | None] | None = ...,
    name: str | None = None,
) -> FixtureFunctionMarker: ...


def fixture(
    fixture_function: FixtureFunction | None = None,
    *,
    scope: ScopeName | Callable[[str, Config], ScopeName] = "function",
    params: Iterable[object] | None = None,
    autouse: bool = False,
    ids: Sequence[object | None] | Callable[[Any], object | None] | None = None,
    name: str | None = None,
) -> FixtureFunctionMarker | FixtureFunctionDefinition:
    """Decorator to mark a fixture factory function.

    This decorator can be used, with or without parameters, to define a
    fixture function.

    The name of the fixture function can later be referenced to cause its
    invocation ahead of running tests: test modules or classes can use the
    ``pytest.mark.usefixtures(fixturename)`` marker.

    Test functions can directly use fixture names as input arguments in which
    case the fixture instance returned from the fixture function will be
    injected.

    Fixtures can provide their values to test functions using ``return`` or
    ``yield`` statements. When using ``yield`` the code block after the
    ``yield`` statement is executed as teardown code regardless of the test
    outcome, and must yield exactly once.

    :param scope:
        The scope for which this fixture is shared; one of ``"function"``
        (default), ``"class"``, ``"module"``, ``"package"`` or ``"session"``.

        This parameter may also be a callable which receives ``(fixture_name, config)``
        as parameters, and must return a ``str`` with one of the values mentioned above.

        See :ref:`dynamic scope` in the docs for more information.

    :param params:
        An optional list of parameters which will cause multiple invocations
        of the fixture function and all of the tests using it. The current
        parameter is available in ``request.param``.

    :param autouse:
        If True, the fixture func is activated for all tests that can see it.
        If False (the default), an explicit reference is needed to activate
        the fixture.

    :param ids:
        Sequence of ids each corresponding to the params so that they are
        part of the test id. If no ids are provided they will be generated
        automatically from the params.

    :param name:
        The name of the fixture. This defaults to the name of the decorated
        function. If a fixture is used in the same module in which it is
        defined, the function name of the fixture will be shadowed by the
        function arg that requests the fixture; one way to resolve this is to
        name the decorated function ``fixture_<fixturename>`` and then use
        ``@pytest.fixture(name='<fixturename>')``.
    """
    fixture_marker = FixtureFunctionMarker(
        scope=scope,
        params=tuple(params) if params is not None else None,
        autouse=autouse,
        ids=None if ids is None else ids if callable(ids) else tuple(ids),
        name=name,
        _ispytest=True,
    )

    # Direct decoration.
    if fixture_function:
        return fixture_marker(fixture_function)

    return fixture_marker

