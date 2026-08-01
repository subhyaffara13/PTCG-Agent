
def _to_flat_tuple(args, kwargs):
    return pytree.arg_tree_leaves(*args, **kwargs)

