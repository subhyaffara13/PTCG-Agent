
def assert_tree_has_only_ndarrays(tree: ArrayTree) -> None:
  """Checks that all `tree`'s leaves are n-dimensional arrays (tensors).

  Args:
    tree: A tree to assert.

  Raises:
    AssertionError: If the tree contains an object which is not an ndarray.
  """
  errors = []

  def _assert_fn(path, leaf):
    if leaf is not None:
      if not isinstance(leaf, (np.ndarray, jnp.ndarray)):
        errors.append((f"Tree leaf '{_ai.format_tree_path(path)}' is not an "
                       f"ndarray (type={type(leaf)})."))

  for path, leaf in jax.tree_util.tree_flatten_with_path(tree)[0]:
    _assert_fn(_ai.convert_jax_path_to_dm_path(path), leaf)
  if errors:
    raise AssertionError("\n".join(errors))

