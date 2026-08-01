
def pytree_path_as_tree_path(path: PyTreePath) -> TreePath:
  """Converts a PyTreePath to a legacy tree path.

  Each PyTreeKey in a PyTreePath has a type specific to the type into which it
  indexes. Legacy tree keys are either strings or integers.

  Args:
    path: The path to be converted.

  Returns:
    A legacy representation of the path.
  """
  return tuple(_pytree_key_as_tree_key(k) for k in path)

