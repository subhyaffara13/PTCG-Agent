
def assert_trees_all_close(actual, desired, rtol=1e-6, atol=0.0, err_msg=None):
  """Asserts that two pytrees of arrays are close within a tolerance."""
  flat_a, tree_def_a = jax.tree_util.tree_flatten(actual)
  flat_d, tree_def_d = jax.tree_util.tree_flatten(desired)
  if tree_def_a != tree_def_d:
    raise AssertionError(
        f"Trees have different structures:\n{tree_def_a}\n{tree_def_d}"
    )
  for x, y in zip(flat_a, flat_d):
    np.testing.assert_allclose(x, y, rtol=rtol, atol=atol, err_msg=err_msg)

