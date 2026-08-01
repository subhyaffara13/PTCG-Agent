
def trace_map(proxy_mode, func_overload, f, xs, pos_args):
    from torch._higher_order_ops.utils import first_slice_copy

    with disable_proxy_modes_tracing():
        # Use first_slice_copy instead of _unstack_pytree to avoid
        # iterating over batch dim, which would guard on symbolic sizes.
        example_input = pytree.tree_map(first_slice_copy, xs)

        body_graph = f

        body_graph = reenter_make_fx(body_graph)(*example_input, *pos_args)

    next_name = proxy_mode.tracer.get_fresh_qualname("body_graph_")

    proxy_mode.tracer.root.register_module(next_name, body_graph)

    fake_outs = map_impl(body_graph, xs, pos_args)

    node_args = (body_graph, list(xs), list(pos_args))
    proxy_args = pytree.tree_map(proxy_mode.tracer.unwrap_proxy, node_args)
    out_proxy = proxy_mode.tracer.create_proxy(
        "call_function", func_overload, proxy_args, {}, name="map_impl"
    )
    return track_tensor_tree(
        fake_outs, out_proxy, constant=None, tracer=proxy_mode.tracer
    )

