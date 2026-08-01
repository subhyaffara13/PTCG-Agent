
def assert_tree_all_finite(actual, err_msg=None):
  """Asserts that all arrays in a pytree are finite."""
  for x in jax.tree_util.tree_leaves(actual):
    if not np.all(np.isfinite(x)):
      raise AssertionError(f"Array {x} is not finite. {err_msg}")

