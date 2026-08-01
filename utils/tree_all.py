
def tree_all(
    pred: Callable[[Any], bool],
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> bool:
    flat_args = tree_iter(tree, is_leaf=is_leaf)
    return all(map(pred, flat_args))


def tree_all(
    pred: Callable[[Any], bool],
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> bool:
    flat_args = tree_iter(tree, is_leaf=is_leaf)
    return all(map(pred, flat_args))


def tree_all(tree: Any, *, is_leaf: Callable[[Any], bool] | None = None) -> bool:
  """Alias of :func:`jax.tree.all`."""
  return all(tree_leaves(tree, is_leaf=is_leaf))

