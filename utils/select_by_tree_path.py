
def select_by_tree_path(
    tree: PyTreeOf[T],
    path: TreePath,
) -> PyTreeOf[T]:
  """Extracts a subtree from a PyTree, using a tree path to describe the path.

  Args:
    tree: The PyTree from which to extract the subtree.
    path: A tuple of keys (str | int) specifying the path to the subtree.

  Returns:
    The subtree.
  """
  match path:
    case (key, *rest):
      keys_and_children, _ = tree_flatten_with_path_one_level(tree)
      for (pytree_key,), child in keys_and_children:
        if _pytree_key_as_tree_key(pytree_key) == key:
          return select_by_tree_path(child, tuple(rest))
      else:
        raise ValueError(f'Path {path} does not exist in {tree=}.')
    case ():
      return tree

