
def tree_leaves(
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> list[Any]:
    """Get the leaves of a pytree.

    See also :func:`tree_flatten`.

    >>> tree = {"b": (2, [3, 4]), "a": 1, "c": None, "d": 5}
    >>> tree_leaves(tree)
    [2, 3, 4, 1, None, 5]
    >>> tree_leaves(1)
    [1]
    >>> tree_leaves(None)
    [None]

    Args:
        tree (pytree): A pytree to flatten.
        is_leaf (callable, optional): An extra leaf predicate function that will be called at each
            flattening step. The function should have a single argument with signature
            ``is_leaf(node) -> bool``. If it returns :data:`True`, the whole subtree being treated
            as a leaf. Otherwise, the default pytree registry will be used to determine a node is a
            leaf or not. If the function is not specified, the default pytree registry will be used.

    Returns:
        A list of leaf values.
    """
    return optree.tree_leaves(
        tree,
        is_leaf=is_leaf,
        none_is_leaf=True,
        namespace="torch",
    )


def tree_leaves(
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> list[Any]:
    """Get a list of leaves of a pytree."""
    return list(tree_iter(tree, is_leaf=is_leaf))


def tree_leaves(
    tree: PyTree,
    /,
    is_leaf: Callable[[PyTree], bool] | None = None,
    *,
    none_is_leaf: bool = False,
    namespace: str = "",
) -> list[Any]:
    return list(
        tree_iter(
            tree,
            is_leaf=is_leaf,
            none_is_leaf=none_is_leaf,
            namespace=namespace,
        )
    )


def tree_leaves(tree: Any,
                is_leaf: Callable[[Any], bool] | None = None
                ) -> list[Leaf]:
  """Alias of :func:`jax.tree.leaves`."""
  return default_registry.flatten(tree, is_leaf)[0]

