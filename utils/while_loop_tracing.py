
def while_loop_tracing(
    mode,
    cond_fn,
    body_fn,
    carried_inputs,
    additional_inputs,
    stack_output=False,
):
    op = while_loop_stack_output_op if stack_output else while_loop_op

    def _trace_while_loop(
        proxy_mode, op, cond_fn, body_fn, carried_inputs, additional_inputs
    ):
        # NOTE [unspecialize int carry with unbacked symints]
        # When we support int carry, we'll also need to support int output of body_fn because.
        # previous iteration's output is next iteration's input and they must match.
        # For carries, when we start tracing while_loop, they can be
        #   - constants e.g. (0, [1, 3])
        #   - backed symints (x.shape[0], [x.shape[1] + x.stride[1], x.shape[2]])
        #   - unbacked symints e.g. (u0, [u0 + u1, u2])
        #   We choose the most conservative design: in all cases, we create new unbacked symints to trace the
        #   subgraph. It's possible to do some analysis on initial carry and the output of first
        #   iteration to determine a better range for the output unbacked symbol e.g. when input is an unbacked
        #   symint >= 0 before the while_loop but in general this is difficult because we don't know
        #   the number of iterations. Users would have to re-constrain the unbacked symint in subgraph if needed.
        #
        # For output of fake cond_fn, it could be constant bool or SymBool (e.g. return x.shape[0] < 4,
        #   where x.shape[0] can be either static of dynamic). In the case of constant bool, we should do a
        #   specialization (NYI).

        # For output of fake body_fn, it could be all three types though from user's point of view,
        # they're all integers e.g.

        #   init_carry = (0, s0, u1, t)
        #   def body_fn(u0, s0, u1, t):
        #     ...
        #     return (t.shape[0], t.shape[1], t.shape[2], y + 1)
        #
        #   It may seem that a constant output isn't possible: users shouldn't write a while_loop
        #   that always return 0. But it could be that a shape is not set as dynamic properly (e.g.
        #   automatic dynamic hasn't been triggered).
        #
        #   For this reason, we treat int, symint outputs in the same way:
        #   - they can match against any of int, symint carry
        #   - we unspecialize them with new unbacked symints in fake while_loop
        #   Similarly, we could do some analysis to refine the output ranges but it's easier to start with
        #   fresh unbacked symints. One surprising case can be: an input unbacked symint is constrained by
        #   users to be >= 0 (either before while_loop or inside body_fn) and it increments by 1 in each
        #   iteration. Ideally, we should know that the final output is >= 0 but we didn't constrain the
        #   unbacked symint output of subgraph as of today because this requires a smart range analysis.
        fake_mode: FakeTensorMode = _find_or_create_fake_mode()

        def _unspecialize_carried_inputs(x):
            if isinstance(x, (int, torch.SymInt)):
                return _create_unbacked_symint(
                    fake_mode, ignore_fresh_unbacked_symbols=True
                )
            # Note: [unspecialize constant tensor carry]
            # We need to disable constant specialization for tensor inputs that become loop carries.
            # Here's the problem: when a user creates a constant tensor e.g. torch.tensor(0), PyTorch calls aten.lift_fresh_copy
            # to create a safe copy (avoiding aliasing issues), which creates a FakeTensor with constant=True.
            # But when this FakeTensor becomes a loop carry, we have a problem:
            # - Operations like .item() will read the constant value and bake it into the traced code
            # - This is incorrect because carry variables change between loop iterations
            # - The traced code would use the wrong constant value for all iterations
            # Solution: We clone the constant tensors and mark the cloned tensor as non-constant so they won't
            # be specialized to fixed values during tracing body_fn or cond_fn.
            elif isinstance(x, torch.Tensor):
                x = x.clone()
                if hasattr(x, "constant") and x.constant is not None:
                    # pyrefly: ignore [missing-attribute]
                    x.constant = None
            return x

        with disable_proxy_modes_tracing():
            unspecialized_carried_inputs = pytree.tree_map_only(
                (int, torch.SymInt, torch.Tensor),
                # For temporarily created unbacked symints, we don't need to bind them to any proxy
                lambda x: _unspecialize_carried_inputs(x),
                carried_inputs,
            )

            def produce_graph(fn):
                cloned_carried_inputs = pytree.tree_map_only(
                    torch.Tensor, lambda x: x.clone(), unspecialized_carried_inputs
                )
                return reenter_make_fx(fn)(*cloned_carried_inputs, *additional_inputs)

            cond_graph = produce_graph(cond_fn)
            body_graph = produce_graph(body_fn)

        next_name = None
        i = 0
        # pyrefly: ignore [bad-assignment]
        while not next_name:
            candidate = f"while_loop_cond_graph_{i}"
            if hasattr(proxy_mode.tracer.root, candidate):
                i += 1
            else:
                next_name = candidate
        cond_graph_name = next_name
        body_graph_name = f"while_loop_body_graph_{i}"
        if hasattr(proxy_mode.tracer.root, body_graph_name):
            raise AssertionError(
                f"proxy_mode.tracer.root already has attribute {body_graph_name}"
            )

        proxy_mode.tracer.root.register_module(cond_graph_name, cond_graph)
        proxy_mode.tracer.root.register_module(body_graph_name, body_graph)

        args = (cond_graph, body_graph, carried_inputs, additional_inputs)

        proxy_args = pytree.tree_map(proxy_mode.tracer.unwrap_proxy, args)

        out_proxy = proxy_mode.tracer.create_proxy(
            "call_function", op, proxy_args, {}, name=op._name
        )

        out = op(
            cond_graph, body_graph, unspecialized_carried_inputs, additional_inputs
        )
        return track_tensor_tree(
            out, out_proxy, constant=None, tracer=proxy_mode.tracer
        )

    return _trace_while_loop(
        mode,
        op,
        cond_fn,
        body_fn,
        carried_inputs,
        additional_inputs,
    )

