
def wrap_combine_fn_flat(*args, combine_fn, spec, num_leaves):
    if len(args) != 2 * num_leaves:
        raise AssertionError(
            f"Combine_fn received wrong number of arguments, expected {2 * num_leaves}, but got {len(args)}"
        )
    lhs = pytree.tree_unflatten(args[:num_leaves], spec)
    rhs = pytree.tree_unflatten(args[num_leaves:], spec)
    return combine_fn(lhs, rhs)


def wrap_combine_fn_flat(
    *args, combine_fn, spec_init, spec_xs, num_init_leaves, num_inp_leaves
):
    if len(args) != (num_init_leaves + num_inp_leaves):
        raise AssertionError(
            f"combine_fn received wrong number of arguments, expected {num_init_leaves + num_inp_leaves}, but got {len(args)}"
        )
    carry = pytree.tree_unflatten(args[:num_init_leaves], spec_init)
    xs = pytree.tree_unflatten(args[num_init_leaves:], spec_xs)
    return combine_fn(carry, xs)

