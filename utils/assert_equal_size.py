
def assert_equal_size(inputs: Sequence[Array]) -> None:
  """Checks that all arrays have the same size.

  Args:
    inputs: A collection of arrays.

  Raises:
    AssertionError: If the size of all arrays do not match.
  """
  _ai.assert_collection_of_arrays(inputs)
  size = inputs[0].size
  expected_sizes = [size] * len(inputs)
  sizes = [x.size for x in inputs]
  if sizes != expected_sizes:
    raise AssertionError(f"Arrays have different sizes: {sizes}")

