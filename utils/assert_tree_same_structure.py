
def assert_tree_same_structure(testclass, expected, actual):
  """Asserts that two PyTrees have the same structure."""
  expected_structure = jax.tree.structure(expected)
  actual_structure = jax.tree.structure(actual)
  testclass.assertEqual(expected_structure, actual_structure)

