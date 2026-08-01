
def tree_is_leaf(
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> bool:
    """Check if a pytree is a leaf.

    >>> tree_is_leaf(1)
    True
    >>> tree_is_leaf(None)
    True
    >>> tree_is_leaf([1, 2, 3])
    False
    >>> tree_is_leaf((1, 2, 3), is_leaf=lambda x: isinstance(x, tuple))
    True
    >>> tree_is_leaf({"a": 1, "b": 2, "c": 3})
    False
    >>> tree_is_leaf({"a": 1, "b": 2, "c": None})
    False

    Args:
        tree (pytree): A pytree to check if it is a leaf node.
        is_leaf (callable, optional): An extra leaf predicate function that will be called at each
            flattening step. The function should have a single argument with signature
            ``is_leaf(node) -> bool``. If it returns :data:`True`, the whole subtree being treated
            as a leaf. Otherwise, the default pytree registry will be used to determine a node is a
            leaf or not. If the function is not specified, the default pytree registry will be used.

    Returns:
        A boolean indicating if the pytree is a leaf node.
    """
    return optree.tree_is_leaf(
        tree,
        is_leaf=is_leaf,
        none_is_leaf=True,
        namespace="torch",
    )


def tree_is_leaf(
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> bool:
    """Check if a pytree is a leaf.

    >>> tree_is_leaf(1)
    True
    >>> tree_is_leaf(None)
    True
    >>> tree_is_leaf([1, 2, 3])
    False
    >>> tree_is_leaf((1, 2, 3), is_leaf=lambda x: isinstance(x, tuple))
    True
    >>> tree_is_leaf({"a": 1, "b": 2, "c": 3})
    False
    >>> tree_is_leaf({"a": 1, "b": 2, "c": None})
    False
    """
    if is_leaf is not None and is_leaf(tree):
        return True
    return _get_node_type(tree) not in SUPPORTED_NODES


def tree_is_leaf(
    tree: PyTree,
    /,
    is_leaf: Callable[[PyTree], bool] | None = None,
    *,
    none_is_leaf: bool = False,
    namespace: str = "",
) -> bool:
    if (tree is None and none_is_leaf) or (is_leaf is not None and is_leaf(tree)):
        return True
    if optree.register_pytree_node.get(type(tree), namespace=namespace) is None:
        return True
    return False

