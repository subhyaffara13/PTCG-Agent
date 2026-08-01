
def assert_trees_all_equal_structs(actual, desired):
  """Asserts that two pytrees have the same structure."""
  if (jax.tree_util.tree_structure(actual) !=
      jax.tree_util.tree_structure(desired)):
    raise AssertionError(
        f"Trees have different structures:\n{actual}\n{desired}"
    )


def assert_trees_all_equal_structs(*trees: ArrayTree) -> None:
  """Checks that trees have the same structure.

  Args:
    *trees: A sequence of (at least 2) trees to assert equal structure between.

  Raises:
    ValueError: If ``trees`` does not contain at least 2 elements.
    AssertionError: If structures of any two trees are different.
  """
  if len(trees) < 2:
    raise ValueError(
        "assert_trees_all_equal_structs on a single tree does not make sense. "
        "Maybe you wrote `assert_trees_all_equal_structs([a, b])` instead of "
        "`assert_trees_all_equal_structs(a, b)` ?")

  first_treedef = jax.tree_util.tree_structure(trees[0])
  other_treedefs = (jax.tree_util.tree_structure(t) for t in trees[1:])
  for i, treedef in enumerate(other_treedefs, start=1):
    if first_treedef != treedef:
      raise AssertionError(
          f"Error in tree structs equality check: trees 0 and {i} do not match,"
          f"\n tree 0: {first_treedef}"
          f"\n tree {i}: {treedef}")

