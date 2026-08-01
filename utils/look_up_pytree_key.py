
def look_up_pytree_key(pytree: PyTreeOf[T], key: PyTreeKey) -> PyTreeOf[T]:
  """Resolves a single PyTree key (i.e. one element of a PyTreePath).

  Args:
    pytree: The PyTree node with respect to which to resolve the key.
    key: The key to resolve.

  Returns:
    An element of the given collection or custom PyTree node.

  Raises:
    KeyError: If the given key is not present in the given node.
  """
  match key:
    case jtu.SequenceKey(idx=k) | jtu.DictKey(key=k):
      try:
        return pytree[k]
      except IndexError as e:
        raise KeyError(f'Key {key!r} not found in {pytree!r}') from e
    case jtu.FlattenedIndexKey(key=k):
      leaves, _ = tree_flatten_with_path_one_level(pytree)
      try:
        idx_and_leaf = leaves[k]
      except IndexError as e:
        raise KeyError(f'Key {key!r} not found in {pytree!r}') from e
      else:
        return idx_and_leaf[1]
    case jtu.GetAttrKey(name=k):
      try:
        return getattr(pytree, k)
      except AttributeError as e:
        raise KeyError(f'Key {key!r} not found in {pytree!r}') from e
  raise KeyError(f'Key {key!r} not found in {pytree!r}')

