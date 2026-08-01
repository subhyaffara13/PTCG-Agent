
def tree_leaves_with_path(
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> list[tuple[KeyPath, Any]]:
    """Gets the leaves of a pytree like ``tree_leaves`` and returns each leaf's key path.

    Args:
        tree: a pytree. If it contains a custom type, that type must be
            registered with an appropriate `tree_flatten_with_path_fn` when registered
            with :func:`register_pytree_node`.
        is_leaf: An extra leaf predicate function that will be called at each
            flattening step. The function should have a single argument with signature
            ``is_leaf(node) -> bool``. If it returns :data:`True`, the whole subtree being treated
            as a leaf. Otherwise, the default pytree registry will be used to determine a node is a
            leaf or not. If the function is not specified, the default pytree registry will be used.
    Returns:
        A list of (key path, leaf) pairs.
    """
    raise NotImplementedError("KeyPaths are not yet supported in cxx_pytree.")


def tree_leaves_with_path(
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> list[tuple[KeyPath, Any]]:
    """Gets the leaves of a pytree like ``tree_leaves`` and returns each leaf's key path.

    Args:
        tree: a pytree. If it contains a custom type, that type must be
            registered with an appropriate `tree_flatten_with_path_fn` when registered
            with :func:`register_pytree_node`.
        is_leaf: An extra leaf predicate function that will be called at each
            flattening step. The function should have a single argument with signature
            ``is_leaf(node) -> bool``. If it returns :data:`True`, the whole subtree being treated
            as a leaf. Otherwise, the default pytree registry will be used to determine a node is a
            leaf or not. If the function is not specified, the default pytree registry will be used.
    Returns:
        A list of (key path, leaf) pairs.
    """
    return list(_generate_key_paths((), tree, is_leaf))


def tree_leaves_with_path(
    tree: Any, is_leaf: Callable[..., bool] | None = None,
    is_leaf_takes_path: bool = False,
) -> list[tuple[KeyPath, Any]]:
  """Alias of :func:`jax.tree.leaves_with_path`."""
  return tree_flatten_with_path(tree, is_leaf, is_leaf_takes_path)[0]

