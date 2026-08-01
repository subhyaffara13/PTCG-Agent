
def handle_sym_dispatch(
    func: Callable[_P, R],
    args: _P.args,  # type: ignore[valid-type]  # not allowed to use _P.args here
    kwargs: _P.kwargs,  # type: ignore[valid-type]  # not allowed to use _P.kwargs here
) -> R:
    """
    Call into the currently active proxy tracing mode to do a
    SymInt/SymFloat/SymBool dispatch trace on a function that operates on
    these arguments.
    """
    mode = get_proxy_mode()
    if not mode:
        raise AssertionError("Expected proxy mode to be set")
    # Have to do it manually, because we're not doing the normal torch
    # dispatch machinery which disables it for us
    with disable_proxy_modes_tracing():
        # TODO: properly compute types
        types: list[type] = []
        return mode.__sym_dispatch__(func, types, args, kwargs)  # type: ignore[arg-type, return-value]

