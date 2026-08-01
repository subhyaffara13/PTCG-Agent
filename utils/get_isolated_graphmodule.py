
def get_isolated_graphmodule(
    func: Callable[..., Any],
    args: tuple[object, ...],
    kwargs: dict[str, object],
    tracing_mode: _TracingMode = "real",
    decomposition_table: Mapping[OpOverload, Callable[..., Any]] | None = None,
) -> GraphModule:
    """A helper function used to get the GraphModule for the given func.

    It's expected to be used in the ProxyTensor tracing context.
    It detaches the args and kwargs from the current tracer so that the trace of
    the current graph module can be created without any side-effects.
    """
    wrapped, all_args = wrapper_and_args_for_make_fx(func, args, kwargs)

    with disable_proxy_modes_tracing():
        gm = make_fx(
            wrapped, decomposition_table=decomposition_table, tracing_mode=tracing_mode
        )(all_args)
    return gm

