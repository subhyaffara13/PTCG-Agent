from typing import Any

def _get_children_with_path(
    path: _KeyPath, node: Any
) -> list[tuple[_KeyPath, Any]]:
  """Get children of a node.

  Private method used in :func:`optax.tree_utils.tree_get_all_with_path` and in
  :func:`optax.tree_utils.tree_set`. In particular, it is tailored for
  nodes that are NamedTuple or dict.

  Args:
    path: path to the node in a pytree.
    node: node in a pytree.

  Returns:
    list of (path_to_child, child) for child a child in nodes.

  Raises:
    ValueError if the given node is not a NamedTuple or a dict
  """
  if _is_named_tuple(node):
    return [
        (
            (*path, NamedTupleKey(node.__class__.__name__, field)),
            getattr(node, field),
        )
        for field in node._fields
    ]
  if isinstance(node, dict):
    return [
        ((*path, jax.tree_util.DictKey(key)), value)
        for key, value in node.items()
    ]
  raise ValueError(
      f"Subtree must be a dict or a NamedTuple. Got {type(node)}"
  )

