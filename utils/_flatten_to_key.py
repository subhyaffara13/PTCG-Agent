
def _flatten_to_key(
    path: _KeyPath, node: Any, key: Any
) -> tuple[_KeyPath, Any]:
  """Flatten a node with a field/key/name matching given key.

  Private method used in :func:`optax.tree_utils.tree_get_all_with_path`.

  Args:
    path: path to the node in a pytree.
    node: node in a pytree.
    key: key to reach for in the node.

  Returns:
    (path_to_key, key_node)
      if key is a key/field of the node,
      ``path_to_key = (*path_to_node, key_path)``, ``key_node = node[key]``,
      otherwise returns the path and node as they are.
  """
  if _is_named_tuple(node):
    if key == node.__class__.__name__:
      return (path, node)
    else:
      path_to_key = (*path, NamedTupleKey(node.__class__.__name__, key))
      return (path_to_key, getattr(node, key))
  if isinstance(node, dict) and key in node:
    return (*path, jax.tree_util.DictKey(key)), node[key]
  return path, node

