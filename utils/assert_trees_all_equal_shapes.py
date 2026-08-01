
def assert_trees_all_equal_shapes(actual, desired, err_msg=None):
  """Asserts that two pytrees of arrays have the same shapes."""
  assert_trees_all_equal_structs(actual, desired)
  for x, y in zip(jax.tree_util.tree_leaves(actual),
                  jax.tree_util.tree_leaves(desired)):
    if x.shape != y.shape:
      raise AssertionError(
          f"Shapes are not equal: {x.shape} != {y.shape}. {err_msg}"
      )


def assert_trees_all_equal_shapes(*trees: ArrayTree) -> None:
  """Checks that trees have the same structure and leaves' shapes.

  Args:
    *trees: A sequence of (at least 2) trees with array leaves.

  Raises:
    AssertionError: If trees' structures or leaves' shapes are different.
  """
  cmp_fn = lambda arr_1, arr_2: arr_1.shape == arr_2.shape
  err_msg_fn = lambda arr_1, arr_2: f"shapes: {arr_1.shape} != {arr_2.shape}"
  assert_trees_all_equal_comparator(cmp_fn, err_msg_fn, *trees)

