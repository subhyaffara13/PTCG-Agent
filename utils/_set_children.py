from typing import Any

def _set_children(node: Any, children_with_keys: dict[Any, Any]) -> Any:
  """Set children of a node.

  Private method used in :func:`optax.tree_utils.tree_set`.
  In particular, it is tailored for nodes that are NamedTuple or dict.

  Args:
    node: node in a pytree.
    children_with_keys: children of the node with associated keys

  Returns:
    new_node whose fields/keys are replaced by the ones given in
    children_with_keys.

  Raises:
    ValueError if the given node is not a NamedTuple or a dict
  """
  if _is_named_tuple(node):
    return node._replace(**children_with_keys)
  if isinstance(node, dict):
    return children_with_keys
  raise ValueError(
      f"Subtree must be a dict or a NamedTuple. Got {type(node)}"
  )

