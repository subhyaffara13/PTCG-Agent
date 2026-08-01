
def map_fake_tensor_mode(mode, f, xs, args):
    from torch._higher_order_ops.utils import first_slice_copy

    with mode:
        # Use first_slice_copy instead of _unstack_pytree to avoid
        # iterating over batch dim, which would guard on symbolic sizes.
        first_row = pytree.tree_map(first_slice_copy, xs)
        example_output = f(*first_row, *args)

        flat_xs, _ = pytree.tree_flatten(xs)
        batch_size = flat_xs[0].shape[0]

        return _broadcast_to_batch(example_output, batch_size)

