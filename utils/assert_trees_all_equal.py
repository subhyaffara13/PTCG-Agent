
def assert_trees_all_equal(actual, desired, err_msg=None):
  """Asserts that two pytrees of arrays are equal."""
  flat_a, tree_def_a = jax.tree_util.tree_flatten(actual)
  flat_d, tree_def_d = jax.tree_util.tree_flatten(desired)
  if tree_def_a != tree_def_d:
    raise AssertionError(
        f"Trees have different structures:\n{tree_def_a}\n{tree_def_d}"
    )
  for x, y in zip(flat_a, flat_d):
    np.testing.assert_array_equal(x, y, err_msg=err_msg)

