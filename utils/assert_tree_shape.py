
def assert_tree_shape(
    tree: ArrayTree, expected_shape: _ai.TShapeMatcher
) -> None:
  """Checks that all ``tree`` leaves match the ``expected_shape``.

  Args:
    tree: A tree to check.
    expected_shape: An expected shape. See ``chex.assert_shape`` for details.

  Raises:
    AssertionError: If some leaf's shape doesn't match ``expected_shape``.
  """
  errors = []

  def _assert_fn(path, leaf):
    if not _shape_matches(leaf.shape, expected_shape):
      errors.append((
          f"Tree leaf '{_ai.format_tree_path(path)}' has shape {leaf.shape}"
          f" but expected {_ai.format_shape_matcher(expected_shape)}."
      ))

  for path, leaf in jax.tree_util.tree_flatten_with_path(tree)[0]:
    _assert_fn(_ai.convert_jax_path_to_dm_path(path), leaf)
  if errors:
    raise AssertionError("\n".join(errors))

