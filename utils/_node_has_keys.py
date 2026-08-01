
def _node_has_keys(node: Any, keys: tuple[Any, ...]) -> bool:
  """Filter for nodes in a tree whose field/key/name matches the given key.

  Private method used in :func:`optax.tree_utils.tree_get_all_with_path` and in
  :func:`optax.tree_utils.tree_set`.

  Args:
    node: node in a pytree.
    keys: keys to search for in the node.

  Returns:
    whether the node has one of the given keys.
  """
  if _is_named_tuple(node) and any(key in node._fields for key in keys):
    return True
  if _is_named_tuple(node) and (node.__class__.__name__ in keys):
    return True
  if isinstance(node, dict) and any(key in node for key in keys):
    return True
  return False

