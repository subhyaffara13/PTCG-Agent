
def trace_aoti_call_delegate(
    proxy_mode, func_overload, lowered_module, original_gm, weight_args, input_args
):
    proxy_mode.tracer.root.register_module("lowered_module", lowered_module)
    proxy_mode.tracer.root.register_module("original_gm", original_gm)

    node_args = (lowered_module, original_gm, weight_args, input_args)
    proxy_args = pytree.tree_map(proxy_mode.tracer.unwrap_proxy, node_args)

    out_proxy = proxy_mode.tracer.create_proxy(
        "call_function", func_overload, proxy_args, {}, name="aoti_call_delegate"
    )
    with disable_proxy_modes_tracing():
        out = call_delegate_cpu(lowered_module, original_gm, weight_args, input_args)

    return track_tensor_tree(out, out_proxy, constant=None, tracer=proxy_mode.tracer)

