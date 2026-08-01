
def reenter_make_fx(fn, subgraph_decomp_table=None):
    from torch.fx.experimental.proxy_tensor import _CURRENT_MAKE_FX_TRACER

    @functools.wraps(fn)
    def wrapped(*args):
        if _CURRENT_MAKE_FX_TRACER is None:
            raise AssertionError(
                "Cannot reenter make_fx when we're not under a make_fx tracing session"
            )
        if subgraph_decomp_table is None:
            gm = _CURRENT_MAKE_FX_TRACER.trace_subgraph(
                _maybe_run_with_interpreter(fn), *args
            )
        else:
            gm = _CURRENT_MAKE_FX_TRACER.trace_subgraph_custom_decomp(
                _maybe_run_with_interpreter(fn), subgraph_decomp_table, *args
            )

        return gm

    return wrapped

