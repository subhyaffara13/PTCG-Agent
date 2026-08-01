
def select_by_pytree_path(
    tree: PyTreeOf[T],
    path: PyTreePath,
) -> PyTreeOf[T]:
  """Extracts a subtree from a PyTree, using a PyTreePath to describe the path.

  Args:
    tree: The PyTree from which to extract the subtree.
    path: A tuple of PyTreeKeys specifying the path to the subtree.

  Returns:
    The subtree.
  """
  match path:
    case (key, *rest):
      try:
        return select_by_pytree_path(look_up_pytree_key(tree, key), tuple(rest))
      except KeyError as e:
        raise ValueError(f'Path {path} does not exist in {tree=}.') from e
    case ():
      return tree

