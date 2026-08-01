
def assert_trees_all_equal_sizes(*trees: ArrayTree) -> None:
  """Checks that trees have the same structure and leaves' sizes.

  Args:
    *trees: A sequence of (at least 2) trees with array leaves.

  Raises:
    AssertionError: If trees' structures or leaves' sizes are different.
  """
  cmp_fn = lambda arr_1, arr_2: arr_1.size == arr_2.size
  err_msg_fn = lambda arr_1, arr_2: f"sizes: {arr_1.size} != {arr_2.size}"
  assert_trees_all_equal_comparator(cmp_fn, err_msg_fn, *trees)

