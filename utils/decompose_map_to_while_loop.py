
def decompose_map_to_while_loop(gm: torch.fx.GraphModule):
    """This is similar to decompose_scan_to_while_loop."""
    graph_pass = PatternMatcherPass()

    @register_graph_pattern(
        CallFunctionVarArgs(torch.ops.higher_order.map_impl),
        # pyrefly: ignore [bad-argument-type]
        pass_dict=graph_pass,
    )
    def _(match: Match, *args, **kwargs):
        assert len(kwargs) == 0, (
            "kwargs of map are not merged into args before entering decompose_map_to_while_loop_pass"
        )
        subgraph, fx_xs, fx_additional_inputs = args
        sub_gm: torch.fx.GraphModule = getattr(gm, subgraph.target)
        cur_node = match.nodes[0]
        mapped_outputs = cur_node.meta["val"]

        def lower_to_while_loop(*args, **kwargs):
            assert len(kwargs) == 0
            xs, additional_inputs = pytree.tree_unflatten(args, tree_spec)
            assert isinstance(xs, (tuple, list)) and isinstance(
                additional_inputs, (tuple, list)
            ), (xs, additional_inputs)
            map_length = xs[0].size(0)
            loop_idx = torch.zeros([], dtype=torch.int64, device=torch.device("cpu"))

            # Similar to NOTE [Pre-allocate scan's output buffer]
            bound_symbols = {
                arg.node.expr: arg
                for arg in pytree.tree_leaves((args, map_length))
                if isinstance(arg, torch.SymInt)
            }
            out_buffers = [
                torch.empty_strided(
                    resolve_shape_to_proxy(out.size(), bound_symbols),
                    resolve_shape_to_proxy(out.stride(), bound_symbols),
                    device=out.device,
                    dtype=out.dtype,
                    layout=out.layout,
                    requires_grad=out.requires_grad,
                )
                for out in mapped_outputs
            ]

            while_loop_operands = (loop_idx, out_buffers, xs)
            while_loop_flat_operands, operands_spec = pytree.tree_flatten(
                while_loop_operands
            )
            while_loop_additional_inputs = additional_inputs
            _, operands_and_additional_inputs_spec = pytree.tree_flatten(
                (*while_loop_operands, additional_inputs)
            )

            def cond_fn(*flat_args):
                loop_idx, _, _, _ = pytree.tree_unflatten(
                    flat_args,
                    operands_and_additional_inputs_spec,
                )
                return loop_idx < map_length

            def body_fn(*flat_args):
                loop_idx, out_bufs, xs, additional_inputs = pytree.tree_unflatten(
                    flat_args,
                    operands_and_additional_inputs_spec,
                )

                idx_int = loop_idx.item()
                torch.ops.aten._assert_scalar.default(idx_int >= 0, "")
                torch.ops.aten._assert_scalar.default(idx_int < map_length, "")
                sub_xs = [torch.ops.aten.select.int(x, 0, idx_int) for x in xs]
                outs = sub_gm(*sub_xs, *additional_inputs)

                for out, buffer in zip(outs, out_bufs):
                    buffer_slice = torch.ops.aten.select.int(buffer, 0, idx_int)
                    buffer_slice.copy_(out)
                return loop_idx + 1, *out_bufs, *xs

            _, final_out, _ = pytree.tree_unflatten(
                torch.ops.higher_order.while_loop(
                    cond_fn,
                    body_fn,
                    tuple(while_loop_flat_operands),
                    tuple(while_loop_additional_inputs),
                ),
                operands_spec,
            )
            return (final_out,)

        lower_to_while_loop_args, tree_spec = pytree.tree_flatten(
            (fx_xs, fx_additional_inputs)
        )
        match.replace_by_example(
            lower_to_while_loop, lower_to_while_loop_args, run_functional_passes=False
        )

    graph_pass.apply(gm)

    for _node in gm.graph.find_nodes(
        op="call_function", target=torch.ops.higher_order.map_impl
    ):
        raise AssertionError("map is not lowered to while_loop")

