from typing import Any, Callable

def leaves_with_path(
    tree: Any, is_leaf: Callable[..., bool] | None = None,
    is_leaf_takes_path: bool = False,
) -> list[tuple[tree_util.KeyPath, Any]]:
  """Gets the leaves of a pytree like ``tree_leaves`` and returns each leaf's key path.

  Args:
    tree: a pytree. If it contains a custom type, it is recommended to be
      registered with ``register_pytree_with_keys``.

  Returns:
    A list of key-leaf pairs, each of which contains a leaf and its key path.

  Examples:
    >>> import jax
    >>> jax.tree.leaves_with_path([1, {'x': 3}])
    [((SequenceKey(idx=0),), 1), ((SequenceKey(idx=1), DictKey(key='x')), 3)]

  See Also:
    - :func:`jax.tree.leaves`
    - :func:`jax.tree.flatten_with_path`
    - :func:`jax.tree_util.register_pytree_with_keys`
  """
  return tree_util.tree_leaves_with_path(tree, is_leaf, is_leaf_takes_path)

