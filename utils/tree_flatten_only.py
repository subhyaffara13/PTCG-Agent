
def tree_flatten_only(ty: type[T], tree: PyTree) -> list[T]:
    flat_vals = pytree.tree_leaves(tree)
    return [elem for elem in flat_vals if isinstance(elem, ty)]

