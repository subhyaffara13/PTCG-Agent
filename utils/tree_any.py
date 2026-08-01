
def tree_any(
    pred: Callable[[Any], bool],
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> bool:
    flat_args = tree_iter(tree, is_leaf=is_leaf)
    return any(map(pred, flat_args))


def tree_any(
    pred: Callable[[Any], bool],
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> bool:
    flat_args = tree_iter(tree, is_leaf=is_leaf)
    return any(map(pred, flat_args))

