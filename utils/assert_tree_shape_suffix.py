
def assert_tree_shape_suffix(
    tree: ArrayTree, shape_suffix: Sequence[int]
) -> None:
  """Checks that all ``tree`` leaves' shapes have the same suffix.

  Args:
    tree: A tree to check.
    shape_suffix: An expected shape suffix.

  Raises:
    AssertionError: If some leaf's shape doesn't end with ``shape_suffix``.
  """
  # To compare with the leaf's `shape`, convert int sequence to tuple.
  shape_suffix = tuple(shape_suffix)

  if not shape_suffix:
    return  # No suffix, this is trivially true.

  errors = []

  def _assert_fn(path, leaf):
    if len(shape_suffix) > len(leaf.shape):
      errors.append(
          (f"Tree leaf '{_ai.format_tree_path(path)}' has a shape "
           f"of length {len(leaf.shape)} (shape={leaf.shape}) which is smaller "
           f"than the expected suffix of length {len(shape_suffix)} "
           f"(suffix={shape_suffix})."))
      return

    suffix = leaf.shape[-len(shape_suffix):]
    if suffix != shape_suffix:
      errors.append(
          (f"Tree leaf '{_ai.format_tree_path(path)}' has a shape suffix "
           f"different from expected: {suffix} != {shape_suffix}."))

  for path, leaf in jax.tree_util.tree_flatten_with_path(tree)[0]:
    _assert_fn(_ai.convert_jax_path_to_dm_path(path), leaf)
  if errors:
    raise AssertionError("\n".join(errors))

