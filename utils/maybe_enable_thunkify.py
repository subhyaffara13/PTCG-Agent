
def maybe_enable_thunkify() -> Generator[None, None, None]:
    """Within this context manager, if you are doing make_fx tracing, we will thunkify
    all SymNode compute and avoid tracing it into the graph unless it is actually needed.
    You should prefer to avoid using this as much as possible, as lazy evaluation of
    SymNode tracing can lead to long chains of thunks which will stack overflow
    if you evaluate them.  However, this is currently sometimes necessary as there
    are buggy parts of PT2 which will fail with "s0 is not tracked with proxy" error
    due to insufficient tracing of SymNode computation.
    """
    proxy_mode = get_proxy_mode()
    if proxy_mode is not None:
        with _enable_thunkify(proxy_mode.tracer):
            yield
    else:
        yield

