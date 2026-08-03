from typing import Any, Callable

def tree_flatten(
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> tuple[list[Any], TreeSpec]:
    """Flatten a pytree.

    See also :func:`tree_unflatten`.

    The flattening order (i.e., the order of elements in the output list) is deterministic,
    corresponding to a left-to-right depth-first tree traversal.

    >>> tree = {"b": (2, [3, 4]), "a": 1, "c": None, "d": 5}
    >>> tree_flatten(tree)
    ([2, 3, 4, 1, None, 5], PyTreeSpec({'b': (*, [*, *]), 'a': *, 'c': *, 'd': *}, NoneIsLeaf, namespace='torch'))
    >>> tree_flatten(1)
    ([1], PyTreeSpec(*, NoneIsLeaf, namespace='torch'))
    >>> tree_flatten(None)
    ([None], PyTreeSpec(*, NoneIsLeaf, namespace='torch'))
    >>> from collections import OrderedDict
    >>> tree = OrderedDict([("b", (2, [3, 4])), ("a", 1), ("c", None), ("d", 5)])
    >>> tree_flatten(tree)
    ([2, 3, 4, 1, None, 5], PyTreeSpec(OrderedDict({'b': (*, [*, *]), 'a': *, 'c': *, 'd': *}), NoneIsLeaf, namespace='torch'))

    Args:
        tree (pytree): A pytree to flatten.
        is_leaf (callable, optional): An extra leaf predicate function that will be called at each
            flattening step. The function should have a single argument with signature
            ``is_leaf(node) -> bool``. If it returns :data:`True`, the whole subtree being treated
            as a leaf. Otherwise, the default pytree registry will be used to determine a node is a
            leaf or not. If the function is not specified, the default pytree registry will be used.

    Returns:
        A pair ``(leaves, treespec)`` where the first element is a list of leaf values and the
        second element is a treespec representing the structure of the pytree.
    """
    return optree.tree_flatten(  # type: ignore[return-value]
        tree,
        is_leaf=is_leaf,
        none_is_leaf=True,
        namespace="torch",
    )


def tree_flatten(
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> tuple[list[Any], TreeSpec]:
    """Flattens a pytree into a list of values and a TreeSpec that can be used
    to reconstruct the pytree.
    """

    def helper(node: PyTree, leaves: list[Any]) -> TreeSpec:
        if tree_is_leaf(node, is_leaf=is_leaf):
            leaves.append(node)
            return _LEAF_SPEC

        node_type = _get_node_type(node)
        flatten_fn = SUPPORTED_NODES[node_type].flatten_fn
        children, context = flatten_fn(node)

        # Recursively flatten the children
        subspecs = [helper(child, leaves) for child in children]
        return TreeSpec(node_type, context, subspecs)

    leaves: list[Any] = []
    treespec = helper(tree, leaves)
    return leaves, treespec


def tree_flatten(
    tree: PyTree,
    /,
    is_leaf: Callable[[PyTree], bool] | None = None,
    *,
    none_is_leaf: bool = False,
    namespace: str = "",
) -> tuple[list[Any], PyTreeSpec]:
    def helper(node: PyTree, leaves: list[Any]) -> PyTreeSpec:
        if tree_is_leaf(
            node,
            is_leaf=is_leaf,
            none_is_leaf=none_is_leaf,
            namespace=namespace,
        ):
            leaves.append(node)
            return PyTreeSpec(
                (),
                None,
                None,
                (),
                None,
                none_is_leaf=none_is_leaf,
                namespace=namespace,
            )

        (
            children,
            metadata,
            entries,
            unflatten_func,
        ) = optree.tree_flatten_one_level(
            node,
            is_leaf=is_leaf,
            none_is_leaf=none_is_leaf,
            namespace=namespace,
        )

        # Recursively flatten the children
        subspecs = tuple(helper(child, leaves) for child in children)
        return PyTreeSpec(
            subspecs,
            type(node),
            metadata,
            entries,
            unflatten_func,  # type: ignore[arg-type]
            none_is_leaf=none_is_leaf,
            namespace=namespace,
        )  # type: ignore[arg-type]

    leaves: list[Any] = []
    treespec = helper(tree, leaves)
    return leaves, treespec


def tree_flatten(tree: Any,
                 is_leaf: Callable[[Any], bool] | None = None
                 ) -> tuple[list[Leaf], PyTreeDef]:
  """Alias of :func:`jax.tree.flatten`."""
  return default_registry.flatten(tree, is_leaf)

