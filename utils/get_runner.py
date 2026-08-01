
def get_runner(
    backend_name: str, backend_options: dict[str, Any]
) -> Iterator[TestRunner]:
    global _current_runner, _runner_leases, _runner_stack
    if _current_runner is None:
        asynclib = get_async_backend(backend_name)
        _runner_stack = ExitStack()
        if current_async_library() is None:
            # Since we're in control of the event loop, we can cache the name of the
            # async library
            token = set_current_async_library(backend_name)
            _runner_stack.callback(reset_current_async_library, token)

        backend_options = backend_options or {}
        _current_runner = _runner_stack.enter_context(
            asynclib.create_test_runner(backend_options)
        )

    _runner_leases += 1
    try:
        yield _current_runner
    finally:
        _runner_leases -= 1
        if not _runner_leases:
            assert _runner_stack is not None
            _runner_stack.close()
            _runner_stack = _current_runner = None

