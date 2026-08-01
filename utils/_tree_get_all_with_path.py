
def _tree_get_all_with_path(
    tree: base.PyTree, key: str
) -> list[tuple[_KeyPath, Any]]:
  """Get all values of a pytree matching a given key.

  Private function called recursively, see
  :func:`optax.tree_utils.tree_get_all_with_path` for public api.

  Args:
    tree: tree to search in.
    key: keyword or name to search in tree for.

  Returns:
    values_with_path
      list of tuples where each tuple is of the form
      (``path_to_value``, ``value``). Here ``value`` is one entry of the tree
      that corresponds to the ``key``, and ``path_to_value`` is a tuple of
      `KeyEntry` that is a tuple of :class:`jax.tree_util.DictKey`,
      :class:`jax.tree_util.FlattenedIndexKey`,
      :class:`jax.tree_util.GetAttrKey`,
      :class:`jax.tree_util.SequenceKey`, or
      :class:`optax.tree_utils.NamedTupleKey`.
  """

  # Get subtrees containing a field with the given key
  has_key = functools.partial(_node_has_keys, keys=(key,))
  leaves_or_subtrees_with_path = _tree_leaves_with_named_tuple_path(
      tree, is_leaf=has_key
  )
  subtrees_with_path = [
      (path, leaf_or_subtree)
      for path, leaf_or_subtree in leaves_or_subtrees_with_path
      if has_key(leaf_or_subtree)
  ]

  # Get (path_to_value, value) for the subtrees found
  found_values_with_path = [
      _flatten_to_key(path, subtree, key)
      for path, subtree in subtrees_with_path
  ]

  # Further search in subtrees for additional values
  for path, subtree in subtrees_with_path:
    children_with_path = _get_children_with_path(path, subtree)
    for path, child in children_with_path:
      new_values_with_path = _tree_get_all_with_path(child, key)
      new_values_with_path = [
          ((*path, *new_path), new_value)
          for new_path, new_value in new_values_with_path
      ]
      found_values_with_path += new_values_with_path
  return found_values_with_path

