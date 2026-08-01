
def scan_batch_rule(interpreter, combine_fn, init, xs, additional_inputs):
    from torch._functorch.vmap import restore_vmap, unwrap_batched, wrap_batched

    unbatched_args, in_dims = unwrap_batched(
        (init, xs, additional_inputs), interpreter.level()
    )
    # move to last dim to not interfere with scan's batching
    unbatched_init, unbatched_xs, unbatched_additional_inputs = pytree.tree_map(
        lambda x, bdim: x.movedim(bdim, -1) if bdim is not None else x,
        unbatched_args,
        in_dims,
    )
    after_move_dims = tuple(
        pytree.tree_flatten(
            pytree.tree_map(lambda x: -1 if x is not None else None, in_dims)
        )[0]
    )

    with interpreter.lower():
        out_dims = None

        def wrapper(*args):
            nonlocal out_dims
            outputs, per_slice_out_dims = restore_vmap(
                combine_fn,
                after_move_dims,
                interpreter.batch_size(),
                interpreter.randomness(),
            )(*args)
            # Note: outputs are not batched, we just move the batch dim to the end
            # this is to avoid it interfering with scan's batching
            outputs = tuple(
                pytree.tree_map(
                    lambda out, out_bdim: out.movedim(out_bdim, -1)
                    if out_bdim is not None
                    else out,
                    outputs,
                    per_slice_out_dims,
                )
            )
            out_dims = tuple(
                pytree.tree_map(
                    lambda out_bdim: -1 if out_bdim is not None else None,
                    per_slice_out_dims,
                )
            )
            return outputs

        unwrapped_out = scan_op(
            wrapper, unbatched_init, unbatched_xs, unbatched_additional_inputs
        )

    if out_dims is None:
        raise AssertionError("out_dims must not be None after scan_op")
    batched_out = wrap_batched(unwrapped_out, out_dims, interpreter.level())
    return batched_out

