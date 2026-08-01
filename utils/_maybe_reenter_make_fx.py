
def _maybe_reenter_make_fx(fn, subgraph_decomp_table=None):
    from torch.fx.experimental.proxy_tensor import _CURRENT_MAKE_FX_TRACER

    if _CURRENT_MAKE_FX_TRACER is not None:
        return reenter_make_fx(fn, subgraph_decomp_table=subgraph_decomp_table)
    else:

        def _maybe_make_fx_with_fake_mode(fn):
            @functools.wraps(fn)
            def wrapped(*args):
                from torch._guards import detect_fake_mode

                fake_mode = detect_fake_mode(args)
                if fake_mode is None:
                    # we creaeta a fake_mode here to make sure we could
                    # trace the graph with data-dependent calls e.g. .item()
                    return make_fx(
                        fn,
                        tracing_mode="fake",
                        decomposition_table=subgraph_decomp_table,
                    )(*args)
                # Tracing with real if all inputs have been fakfied
                return make_fx(fn, decomposition_table=subgraph_decomp_table)(*args)

            return wrapped

        return _maybe_make_fx_with_fake_mode(fn)

