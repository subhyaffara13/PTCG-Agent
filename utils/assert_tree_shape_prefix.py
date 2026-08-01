
def assert_tree_shape_prefix(tree: ArrayTree,
                             shape_prefix: Sequence[int]) -> None:
  """Checks that all ``tree`` leaves' shapes have the same prefix.

  Args:
    tree: A tree to check.
    shape_prefix: An expected shape prefix.

  Raises:
    AssertionError: If some leaf's shape doesn't start with ``shape_prefix``.
  """
  # To compare with the leaf's `shape`, convert int sequence to tuple.
  shape_prefix = tuple(shape_prefix)

  if not shape_prefix:
    return  # No prefix, this is trivially true.

  errors = []

  def _assert_fn(path, leaf):
    if len(shape_prefix) > len(leaf.shape):
      errors.append(
          (f"Tree leaf '{_ai.format_tree_path(path)}' has a shape "
           f"of length {leaf.ndim} (shape={leaf.shape}) which is smaller "
           f"than the expected prefix of length {len(shape_prefix)} "
           f"(prefix={shape_prefix})."))
      return

    suffix = leaf.shape[:len(shape_prefix)]
    if suffix != shape_prefix:
      errors.append(
          (f"Tree leaf '{_ai.format_tree_path(path)}' has a shape prefix "
           f"different from expected: {suffix} != {shape_prefix}."))

  for path, leaf in jax.tree_util.tree_flatten_with_path(tree)[0]:
    _assert_fn(_ai.convert_jax_path_to_dm_path(path), leaf)
  if errors:
    raise AssertionError("\n".join(errors))

