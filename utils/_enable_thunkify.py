
def _enable_thunkify(
    tracer: _ProxyTracer, *, enable: bool = True
) -> Generator[None, None, None]:
    """
    Enable thunkification inside the context manager.  Thunkification prevents
    SymNode computation from directly being traced into an FX graph; instead,
    the compute is only added to the graph if it is actually used.  This helps
    us track SymNode compute when it is computed (since we need /something/
    to put in the tracker) even if it is unlikely to be used.
    """
    old = tracer.enable_thunkify
    tracer.enable_thunkify = enable
    try:
        yield
    finally:
        tracer.enable_thunkify = old

