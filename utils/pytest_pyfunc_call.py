from typing import Any

def pytest_pyfunc_call(pyfuncitem):  # type: ignore[no-untyped-def]
    """Run coroutines in an event loop instead of a normal function call."""
    fast = pyfuncitem.config.getoption("--aiohttp-fast")
    if inspect.iscoroutinefunction(pyfuncitem.function):
        warnings.warn(
            "aiohttp.pytest_plugin will be removed in v4. Please install pytest-aiohttp.",
            DeprecationWarning,
        )
        existing_loop = (
            pyfuncitem.funcargs.get("proactor_loop")
            or pyfuncitem.funcargs.get("selector_loop")
            or pyfuncitem.funcargs.get("uvloop_loop")
            or pyfuncitem.funcargs.get("loop", None)
        )

        with _runtime_warning_context():
            with _passthrough_loop_context(existing_loop, fast=fast) as _loop:
                testargs = {
                    arg: pyfuncitem.funcargs[arg]
                    for arg in pyfuncitem._fixtureinfo.argnames
                }
                _loop.run_until_complete(pyfuncitem.obj(**testargs))

        return True


def pytest_pyfunc_call(pyfuncitem: Any) -> bool | None:
    def run_with_hypothesis(**kwargs: Any) -> None:
        with get_runner(backend_name, backend_options) as runner:
            runner.run_test(original_func, kwargs)

    backend = pyfuncitem.funcargs.get("anyio_backend")
    if backend:
        backend_name, backend_options = extract_backend_and_options(backend)

        if hasattr(pyfuncitem.obj, "hypothesis"):
            # Wrap the inner test function unless it's already wrapped
            original_func = pyfuncitem.obj.hypothesis.inner_test
            if original_func.__qualname__ != run_with_hypothesis.__qualname__:
                if iscoroutinefunction(original_func):
                    pyfuncitem.obj.hypothesis.inner_test = run_with_hypothesis

            return None

        if iscoroutinefunction(pyfuncitem.obj):
            funcargs = pyfuncitem.funcargs
            testargs = {arg: funcargs[arg] for arg in pyfuncitem._fixtureinfo.argnames}
            with get_runner(backend_name, backend_options) as runner:
                try:
                    runner.run_test(pyfuncitem.obj, testargs)
                except ExceptionGroup as excgrp:
                    for exc in iterate_exceptions(excgrp):
                        if isinstance(exc, (Exit, KeyboardInterrupt, SystemExit)):
                            raise exc from excgrp

                    raise

            return True

    return None


def pytest_pyfunc_call(pyfuncitem: Function) -> object | None:
    """Call underlying test function.

    Stops at first non-None result, see :ref:`firstresult`.

    :param pyfuncitem:
        The function item.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given item, only
    conftest files in the item's directory and its parent directories
    are consulted.
    """


def pytest_pyfunc_call(pyfuncitem: Function) -> object | None:
    testfunction = pyfuncitem.obj
    if is_async_function(testfunction):
        async_fail(pyfuncitem.nodeid)
    funcargs = pyfuncitem.funcargs
    testargs = {arg: funcargs[arg] for arg in pyfuncitem._fixtureinfo.argnames}
    result = testfunction(**testargs)
    if hasattr(result, "__await__") or hasattr(result, "__aiter__"):
        async_fail(pyfuncitem.nodeid)
    elif result is not None:
        warnings.warn(
            PytestReturnNotNoneWarning(
                f"Test functions should return None, but {pyfuncitem.nodeid} returned {type(result)!r}.\n"
                "Did you mean to use `assert` instead of `return`?\n"
                "See https://docs.pytest.org/en/stable/how-to/assert.html#return-not-none for more information."
            )
        )
    return True

