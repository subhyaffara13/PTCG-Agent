
def while_loop_fake_tensor_mode(
    mode, cond_fn, body_fn, carried_inputs, additional_inputs, stack_output=False
):
    with mode:
        # NOTE: [Handling unback symints in subgraph of while_loop]
        # The idea is that the scope of unbacked symints are limited to the subgraph.
        #
        # We're implementing the fake tensor mode of while_loop operator.
        # and we run body_fn once to get an fake output.
        # Let's first consider the case that unbacked symints are tensor shapes:
        #
        # Case 1:
        # if the unbacked symints is local to the subgraph e.g.
        #   def body_fn(it, x):
        #     nz = x.nonzero()
        #     return it+1. nz.sum()
        # we can just ignore the newly created unbacked symints because it has
        # no effect on the output of while_loop and it's tracked when we tracing.
        # the subgraph.
        #
        # Case 2:
        # if the unbacked symints are shape of output of while_loop e.g.
        #   def body_fn(it, x):
        #     nz = x.nonzero()
        #     return it+1, nz
        # This will fail the shape check because in each iteration, the carried_input's shape
        # must match the output shape as nz.shape contains newly allocated unbacked symint, this
        # won't match the carried_input's shape.
        #
        # Case 3:
        # if the unbacked symints are shape of carried_inputs e.g.
        #   nz = a.nonzero()
        #   body_fn(it, nz):
        #     return it+1. nz.sin() + 1,
        # There's no new unbacked symints allocated in subgraph, so we're safe.
        with mode.shape_env.ignore_fresh_unbacked_symbols():
            # body_fn return output with the same pytree and tensor meta data as carried_inputs
            # so we could just return the output after one iteration.
            body_outs = body_fn(*carried_inputs, *additional_inputs)
            check_meta_consistency(
                carried_inputs,
                body_outs,
                "carried_inputs",
                "body_output",
                include_contiguity=False,
            )

        if stack_output:
            n_iter = _create_unbacked_symint(mode, ignore_fresh_unbacked_symbols=False)
            if not all(isinstance(x, torch.Tensor) for x in carried_inputs):
                raise AssertionError(
                    f"all carried_inputs must be tensors for stack_output, got {[type(x) for x in carried_inputs]}"
                )
            fake_outputs = tuple(
                out.clone()
                .unsqueeze(0)
                .repeat((n_iter,) + tuple(1 for _ in range(out.dim())))
                for out in body_outs
            )
            return pytree.tree_map_only(
                (int, torch.SymInt),
                # For while_loop's unbacked symint output, we want them to be bound
                # to the proxy of while_loop's output.
                lambda _: _create_unbacked_symint(
                    mode, ignore_fresh_unbacked_symbols=False
                ),
                fake_outputs,
            )

        # See NOTE [unspecialize int carry with unbacked symints]
        return pytree.tree_map_only(
            (int, torch.SymInt),
            # For while_loop's unbacked symint output, we want them to be bound
            # to the proxy of while_loop's output.
            lambda _: _create_unbacked_symint(
                mode, ignore_fresh_unbacked_symbols=False
            ),
            body_outs,
        )

