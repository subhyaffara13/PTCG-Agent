
def tree_structure(
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> TreeSpec:
    """Get the treespec for a pytree.

    See also :func:`tree_flatten`.

    >>> tree = {"b": (2, [3, 4]), "a": 1, "c": None, "d": 5}
    >>> tree_structure(tree)
    PyTreeSpec({'b': (*, [*, *]), 'a': *, 'c': *, 'd': *}, NoneIsLeaf, namespace='torch')
    >>> tree_structure(1)
    PyTreeSpec(*, NoneIsLeaf, namespace='torch')
    >>> tree_structure(None)
    PyTreeSpec(*, NoneIsLeaf, namespace='torch')

    Args:
        tree (pytree): A pytree to flatten.
        is_leaf (callable, optional): An extra leaf predicate function that will be called at each
            flattening step. The function should have a single argument with signature
            ``is_leaf(node) -> bool``. If it returns :data:`True`, the whole subtree being treated
            as a leaf. Otherwise, the default pytree registry will be used to determine a node is a
            leaf or not. If the function is not specified, the default pytree registry will be used.

    Returns:
        A treespec object representing the structure of the pytree.
    """
    return optree.tree_structure(  # type: ignore[return-value]
        tree,
        is_leaf=is_leaf,
        none_is_leaf=True,
        namespace="torch",
    )


def tree_structure(
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> TreeSpec:
    """Get the TreeSpec for a pytree."""
    return tree_flatten(tree, is_leaf=is_leaf)[1]


def tree_structure(
    tree: PyTree,
    /,
    is_leaf: Callable[[PyTree], bool] | None = None,
    *,
    none_is_leaf: bool = False,
    namespace: str = "",
) -> PyTreeSpec:
    return tree_flatten(  # type: ignore[return-value]
        tree,
        is_leaf=is_leaf,
        none_is_leaf=none_is_leaf,
        namespace=namespace,
    )[1]


def tree_structure(tree: Any,
                   is_leaf: None | (Callable[[Any],
                                              bool]) = None) -> PyTreeDef:
  """Alias of :func:`jax.tree.structure`."""
  return default_registry.flatten(tree, is_leaf)[1]

