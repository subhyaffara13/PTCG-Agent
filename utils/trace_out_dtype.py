
def trace_out_dtype(proxy_mode, func_overload, op, output_dtype, *args):
    # NB: Long-term we should put the decomposition logic into
    # ProxyTorchDispatchMode so that people do not need to call maybe_handle_decomp
    # in all HigherOrderOp proxy implementations.
    r = maybe_handle_decomp(proxy_mode, func_overload, (op, output_dtype, *args), {})
    if r is not NotImplemented:
        return r

    with disable_proxy_modes_tracing():
        # This is a simplified implementation of this operator just for tracing.
        # Actual implementation may also first promote the arguments
        out = op(*args).to(dtype=output_dtype)

    node_args = (op, output_dtype, *args)
    proxy_args = pytree.tree_map(proxy_mode.tracer.unwrap_proxy, node_args)
    out_proxy = proxy_mode.tracer.create_proxy(
        "call_function", func_overload, proxy_args, {}, name="out_dtype"
    )
    return track_tensor_tree(out, out_proxy, constant=None, tracer=proxy_mode.tracer)

