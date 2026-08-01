
def from_graphable(
    flat_args: tuple[Unpack[_Ts]], spec: pytree.TreeSpec
) -> pytree.PyTree:
    """The inverse of to_graphable."""
    stuff = pytree.tree_unflatten(flat_args, spec)
    return stuff

