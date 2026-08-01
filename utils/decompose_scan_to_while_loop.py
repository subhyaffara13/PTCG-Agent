
def decompose_scan_to_while_loop(gm: torch.fx.GraphModule):
    """
    NOTE [decompose scan to while_loop]
    This pass decomposes `scan` to  `while_loop` by replacing the scan fx_node with a while_loop hop.

    Suppose we have a function f:

        def f():
            init = torch.zeros([])
            xs = torch.arange(4)
            ys = []
            for i in range(xs.size(0)):
                init = xs[i] + init
                ys.append(init)

            # Return the final carry and stack the intermediates
            return init, torch.stack(ys)

    We could rewrite it with a scan with the benefits of reducing compilation time/binary size, reducing
    memory usage, supporting loops over unbacked shapes and cudagraph etc.

        def g():
            def step_fn(init: torch.Tensor, x: torch.Tensor):
                next_init = x + init
                return next_init, next_init

            init = torch.zeros([])
            xs = torch.arange(4)
            final_carry, ys = torch._higher_order.scan(step_fn, init, xs)
            return final_carry, ys

    This pass will rewrite scan into:

        def k():
            init = torch.zeros([])
            xs = torch.arange(4)

            # we create a loop_idx and loop through xs.shape[0]
            loop_idx = torch.zeros([])
            ys = torch.empty_strided(_shape_stride_of_ys)
            def cond_fn(loop_idx, ys, init, xs):
                return loop_idx < xs.shape[0]

            # we pre-allocate the output buffer ys and inplace
            # copy the y of each intermediate into a slice.
            # NOTE [Pre-allocate scan's output buffer].
            def body_fn(loop_idx, ys, init, xs):
                int_idx = loop_idx.item()
                next_init, y = step_fn(init, xs[int_idx])
                ys[int_idx].copy_(y)
                return loop_idx + 1, ys, next_init, xs

            final_carry, _, _, ys = torch._higher_order.while_loop(cond_fn, body_fn, (loop_idx, ys, init, xs))
            return final_carry, ys
    """

    graph_pass = PatternMatcherPass()

    @register_graph_pattern(
        CallFunctionVarArgs(torch.ops.higher_order.scan),
        # pyrefly: ignore [bad-argument-type]
        pass_dict=graph_pass,
    )
    def _(match: Match, *args, **kwargs):
        from torch._higher_order_ops.scan import _extract_carry_and_out

        assert len(kwargs) == 0, (
            "kwargs of scan are not merged into args before entering decompose_scan_to_while_loop_pass"
        )

        combine_subgraph, fx_init, fx_xs, fx_additional_inputs = args
        assert combine_subgraph.op == "get_attr", "first arg is not combine_subgraph"
        sub_gm: torch.fx.GraphModule = getattr(gm, combine_subgraph.target)
        cur_node = match.nodes[0]
        num_init_leaves = len(fx_init)
        _, ys_outputs = _extract_carry_and_out(cur_node.meta["val"], num_init_leaves)

        def lower_to_while_loop(*args, **kwargs):
            """
            The traced graph of this function will be used to replace the original scan fx_node.
            """
            assert len(kwargs) == 0

            # Step 1: construct necessary inputs to while_loop based on scan's input.
            (
                init,
                xs,
                additional_inputs,
            ) = pytree.tree_unflatten(args, tree_spec)
            scan_length = xs[0].size(0)
            loop_idx = torch.zeros([], dtype=torch.int64, device=torch.device("cpu"))

            # NOTE [Pre-allocate scan's output buffer]
            # In order to pre-allocate the output buffer for ys, we rely on the meta of scan's fx_node.
            # However, the meta consists of concrete symints, we need to bind those symints with
            # proxies in order to trace the torch.empty_strided call correctly.
            #
            # Also note that basic free symbols of tensor's shapes are guaranteed to be lifted as subgraph inputs
            # in dynamo so we can always re-construct the sym expression from placeholders.
            # See Note [Auto lift basic free symbols when create_graph_input] for how this is done.
            bound_symbols = {
                arg.node.expr: arg
                for arg in pytree.tree_leaves((args, scan_length))
                if isinstance(arg, torch.SymInt)
            }
            ys_outs = [
                torch.empty_strided(
                    resolve_shape_to_proxy(ys_out.size(), bound_symbols),
                    resolve_shape_to_proxy(ys_out.stride(), bound_symbols),
                    device=ys_out.device,
                    dtype=ys_out.dtype,
                    layout=ys_out.layout,
                    requires_grad=ys_out.requires_grad,
                )
                for ys_out in ys_outputs
            ]

            while_loop_operands = (loop_idx, ys_outs, init, xs)
            flat_operands, operands_spec = pytree.tree_flatten(while_loop_operands)
            _, operands_and_additional_inputs_spec = pytree.tree_flatten(
                (*while_loop_operands, additional_inputs)
            )

            # Step 2: create the cond_fn and body_fn for while_loop
            def cond_fn(*flat_args):
                loop_idx, _, _, _, _ = pytree.tree_unflatten(
                    flat_args, operands_and_additional_inputs_spec
                )  # type: ignore[has-type]
                return loop_idx < scan_length  # type: ignore[has-type]

            def body_fn(*flat_args):
                loop_idx, ys_outs, carry, xs, additional_inputs = pytree.tree_unflatten(
                    flat_args,
                    operands_and_additional_inputs_spec,  # type: ignore[has-type]
                )

                idx_int = loop_idx.item()
                torch.ops.aten._assert_scalar.default(idx_int >= 0, "")
                torch.ops.aten._assert_scalar.default(idx_int < scan_length, "")
                sub_xs = [torch.ops.aten.select.int(x, 0, idx_int) for x in xs]
                next_carry, ys = _extract_carry_and_out(
                    sub_gm(*(list(carry) + sub_xs + list(additional_inputs))),
                    num_init_leaves,
                )
                for y, y_out in zip(ys, ys_outs):
                    y_out_slice = torch.ops.aten.select.int(y_out, 0, idx_int)
                    y_out_slice.copy_(y)
                return loop_idx + 1, *ys_outs, *next_carry, *xs

            # Step 3: call the while_loop operator
            _, ys_outs, last_carry, _ = pytree.tree_unflatten(
                torch.ops.higher_order.while_loop(
                    cond_fn,
                    body_fn,
                    tuple(flat_operands),
                    tuple(additional_inputs),
                ),
                operands_spec,
            )
            return list(last_carry) + list(ys_outs)

        lower_to_while_loop_args, tree_spec = pytree.tree_flatten(
            (
                fx_init,
                fx_xs,
                fx_additional_inputs,
            )
        )
        match.replace_by_example(
            lower_to_while_loop,
            lower_to_while_loop_args,
            run_functional_passes=False,
        )

    graph_pass.apply(gm)

    for _node in gm.graph.find_nodes(
        op="call_function", target=torch.ops.higher_order.scan
    ):
        raise AssertionError("scan is not lowered to while_loop")

