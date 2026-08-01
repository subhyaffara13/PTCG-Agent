
def pytest_fixture_setup(fixturedef):  # type: ignore[no-untyped-def]
    """Set up pytest fixture.

    Allow fixtures to be coroutines. Run coroutine fixtures in an event loop.
    """
    func = fixturedef.func

    if inspect.isasyncgenfunction(func):
        # async generator fixture
        is_async_gen = True
    elif inspect.iscoroutinefunction(func):
        # regular async fixture
        is_async_gen = False
    else:
        # not an async fixture, nothing to do
        return

    strip_request = False
    if "request" not in fixturedef.argnames:
        fixturedef.argnames += ("request",)
        strip_request = True

    def wrapper(*args, **kwargs):  # type: ignore[no-untyped-def]
        request = kwargs["request"]
        if strip_request:
            del kwargs["request"]

        # if neither the fixture nor the test use the 'loop' fixture,
        # 'getfixturevalue' will fail because the test is not parameterized
        # (this can be removed someday if 'loop' is no longer parameterized)
        if "loop" not in request.fixturenames:
            raise Exception(
                "Asynchronous fixtures must depend on the 'loop' fixture or "
                "be used in tests depending from it."
            )

        _loop = request.getfixturevalue("loop")

        if is_async_gen:
            # for async generators, we need to advance the generator once,
            # then advance it again in a finalizer
            gen = func(*args, **kwargs)

            def finalizer():  # type: ignore[no-untyped-def]
                try:
                    return _loop.run_until_complete(gen.__anext__())
                except StopAsyncIteration:
                    pass

            request.addfinalizer(finalizer)
            return _loop.run_until_complete(gen.__anext__())
        else:
            return _loop.run_until_complete(func(*args, **kwargs))

    fixturedef.func = wrapper


def pytest_fixture_setup(fixturedef: Any, request: Any) -> Generator[Any]:
    def wrapper(anyio_backend: Any, request: SubRequest, **kwargs: Any) -> Any:
        # Rebind any fixture methods to the request instance
        if (
            request.instance
            and ismethod(func)
            and type(func.__self__) is type(request.instance)
        ):
            local_func = func.__func__.__get__(request.instance)
        else:
            local_func = func

        backend_name, backend_options = extract_backend_and_options(anyio_backend)
        if has_backend_arg:
            kwargs["anyio_backend"] = anyio_backend

        if has_request_arg:
            kwargs["request"] = request

        with get_runner(backend_name, backend_options) as runner:
            # re-entrant call into the test runner detected. this happens when an async fixture
            # is dynamically requested via request.getfixturevalue() from inside a running async
            # test or fixture. on asyncio this raises RuntimeError: This event loop is already
            # running, on trio the runner deadlocks - the host loop blocks waiting for the
            # coroutine to return, but the coroutine is waiting for the host loop. raising here
            # prevents the hang and gives a consistent error across backends.
            if runner.is_running():
                raise RuntimeError(
                    "Cannot schedule a coroutine in the test runner while another is already running; "
                    "likely caused by request.getfixturevalue() on an async fixture."
                )

            if isasyncgenfunction(local_func):
                yield from runner.run_asyncgen_fixture(local_func, kwargs)
            else:
                yield runner.run_fixture(local_func, kwargs)

    # Only apply this to coroutine functions and async generator functions in requests
    # that involve the anyio_backend fixture
    func = fixturedef.func
    if isasyncgenfunction(func) or iscoroutinefunction(func):
        if "anyio_backend" in request.fixturenames:
            fixturedef.func = wrapper
            original_argname = fixturedef.argnames

            if not (has_backend_arg := "anyio_backend" in fixturedef.argnames):
                fixturedef.argnames += ("anyio_backend",)

            if not (has_request_arg := "request" in fixturedef.argnames):
                fixturedef.argnames += ("request",)

            try:
                return (yield)
            finally:
                fixturedef.func = func
                fixturedef.argnames = original_argname

    return (yield)


def pytest_fixture_setup(
    fixturedef: FixtureDef[FixtureValue], request: SubRequest
) -> FixtureValue:
    """Execution of fixture setup."""
    kwargs = {}
    for argname in fixturedef.argnames:
        kwargs[argname] = request.getfixturevalue(argname)

    fixturefunc = resolve_fixture_function(fixturedef, request)
    my_cache_key = fixturedef.cache_key(request)

    if inspect.isasyncgenfunction(fixturefunc) or inspect.iscoroutinefunction(
        fixturefunc
    ):
        auto_str = " with autouse=True" if fixturedef._autouse else ""
        fail(
            f"{request.node.name!r} requested an async fixture {request.fixturename!r}{auto_str}, "
            "with no plugin or hook that handled it. This is an error, as pytest does not natively support it.\n"
            "See: https://docs.pytest.org/en/stable/deprecations.html#sync-test-depending-on-async-fixture",
            pytrace=False,
        )

    try:
        result = call_fixture_func(fixturefunc, request, kwargs)
    except TEST_OUTCOME as e:
        if isinstance(e, skip.Exception):
            # The test requested a fixture which caused a skip.
            # Don't show the fixture as the skip location, as then the user
            # wouldn't know which test skipped.
            e._use_item_location = True
        fixturedef.cached_result = (None, my_cache_key, (e, e.__traceback__))
        raise
    fixturedef.cached_result = (result, my_cache_key, None)
    return result


def pytest_fixture_setup(
    fixturedef: FixtureDef[Any], request: SubRequest
) -> object | None:
    """Perform fixture setup execution.

    :param fixturedef:
        The fixture definition object.
    :param request:
        The fixture request object.
    :returns:
        The return value of the call to the fixture function.

    Stops at first non-None result, see :ref:`firstresult`.

    .. note::
        If the fixture function returns None, other implementations of
        this hook function will continue to be called, according to the
        behavior of the :ref:`firstresult` option.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given fixture, only
    conftest files in the fixture scope's directory and its parent directories
    are consulted.
    """


def pytest_fixture_setup(
    fixturedef: FixtureDef[object], request: SubRequest
) -> Generator[None, object, object]:
    try:
        return (yield)
    finally:
        if request.config.option.setupshow:
            if hasattr(request, "param"):
                # Save the fixture parameter so ._show_fixture_action() can
                # display it now and during the teardown (in .finish()).
                if fixturedef.ids:
                    if callable(fixturedef.ids):
                        param = fixturedef.ids(request.param)
                    else:
                        param = fixturedef.ids[request.param_index]
                else:
                    param = request.param
                fixturedef.cached_param = param  # type: ignore[attr-defined]
            _show_fixture_action(fixturedef, request.config, "SETUP")


def pytest_fixture_setup(
    fixturedef: FixtureDef[object], request: SubRequest
) -> object | None:
    # Will return a dummy fixture if the setuponly option is provided.
    if request.config.option.setupplan:
        my_cache_key = fixturedef.cache_key(request)
        fixturedef.cached_result = (None, my_cache_key, None)
        return fixturedef.cached_result
    return None

