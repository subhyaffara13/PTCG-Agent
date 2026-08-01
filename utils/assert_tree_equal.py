
def assert_tree_equal(testclass, expected, actual):
  """Asserts that two PyTrees are equal."""
  expected_flat = tree_utils.to_flat_dict(expected)
  actual_flat = tree_utils.to_flat_dict(actual)
  testclass.assertSameElements(expected_flat.keys(), actual_flat.keys())

  def _eq(x, y):
    if x is None:
      return
    assert_array_equal(testclass, x, y)

  jax.tree.map(_eq, expected, actual, is_leaf=lambda x: x is None)

