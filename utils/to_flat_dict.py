
def to_flat_dict(
    tree: PyTree,
    sep: Optional[str] = None,
    keep_empty_nodes: bool = False,
    is_leaf: Optional[Callable[[Any], bool]] = None,
) -> PyTree:
  """Converts a tree into a flattened dictionary.

  The nested keys are flattened to a tuple.

  Example::

    tree = {'foo': 1, 'bar': {'a': 2, 'b': {}}}
    to_flat_dict(tree)
    {
      ('foo',): 1,
      ('bar', 'a'): 2,
    }

  Args:
    tree: A PyTree to be flattened.
    sep: If provided, keys will be returned as `sep`-separated strings.
      Otherwise, keys are returned as tuples.
    keep_empty_nodes: If True, empty nodes are not filtered out.
    is_leaf: If provided, a function that returns True if a value is a leaf.
      Overrides `keep_empty_nodes` if that is also provided.

  Returns:
    A flattened dictionary and the tree structure.
  """
  is_leaf = is_leaf or (is_empty_or_leaf if keep_empty_nodes else None)
  flat_with_keys, _ = jax.tree_util.tree_flatten_with_path(
      tree, is_leaf=is_leaf
  )
  flat_dict = {tuple_path_from_keypath(k): v for k, v in flat_with_keys}
  if sep is not None:
    flat_dict = {sep.join(k): v for k, v in flat_dict.items()}
  return flat_dict

