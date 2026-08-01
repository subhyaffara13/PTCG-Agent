
def is_tree_node(typ: type) -> bool:
  """Returns True if the type is a registered PyTree node type.

  Args:
    typ: The type to check.

  Returns:
    True if the type is a registered PyTree node type (built-in or custom)
    or a namedtuple type.
  """
  return default_registry.is_node(typ)


def is_tree_node(x):
  return isinstance(x, NodeStates)

