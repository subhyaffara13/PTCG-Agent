from typing import Any, Callable

def flatten_with_path(
    tree: Any, is_leaf: Callable[..., bool] | None = None,
    is_leaf_takes_path: bool = False,
) -> tuple[list[tuple[tree_util.KeyPath, Any]], tree_util.PyTreeDef]:
  """Flattens a pytree like ``tree_flatten``, but also returns each leaf's key path.

  Args:
    tree: a pytree to flatten. If it contains a custom type, it is recommended
      to be registered with ``register_pytree_with_keys``.

  Returns:
    A pair which the first element is a list of key-leaf pairs, each of
    which contains a leaf and its key path. The second element is a treedef
    representing the structure of the flattened tree.

  Examples:
    >>> import jax
    >>> path_vals, treedef = jax.tree.flatten_with_path([1, {'x': 3}])
    >>> path_vals
    [((SequenceKey(idx=0),), 1), ((SequenceKey(idx=1), DictKey(key='x')), 3)]
    >>> treedef
    PyTreeDef([*, {'x': *}])

  See Also:
    - :func:`jax.tree.flatten`
    - :func:`jax.tree.map_with_path`
    - :func:`jax.tree_util.register_pytree_with_keys`
  """
  return tree_util.tree_flatten_with_path(tree, is_leaf, is_leaf_takes_path)

