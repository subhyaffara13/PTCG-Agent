
def unittest_run_loop(func: Any, *args: Any, **kwargs: Any) -> Any:
    """
    A decorator dedicated to use with asynchronous AioHTTPTestCase test methods.

    In 3.8+, this does nothing.
    """
    warnings.warn(
        "Decorator `@unittest_run_loop` is no longer needed in aiohttp 3.8+",
        DeprecationWarning,
        stacklevel=2,
    )
    return func

