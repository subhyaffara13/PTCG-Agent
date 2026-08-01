
def assert_equal_shape_prefix(inputs: Sequence[Array], prefix_len: int) -> None:
  """Checks that the leading ``prefix_dims`` dims of all inputs have same shape.

  Args:
    inputs: A collection of input arrays.
    prefix_len: A number of leading dimensions to compare; each input's shape
      will be sliced to ``shape[:prefix_len]``. Negative values are accepted and
      have the conventional Python indexing semantics.

  Raises:
    AssertionError: If the shapes of all arrays do not match.
    ValuleError: If ``inputs`` is not a collection of arrays.
  """
  _ai.assert_collection_of_arrays(inputs)

  shapes = [array.shape[:prefix_len] for array in inputs]
  if shapes != [shapes[0]] * len(shapes):
    raise AssertionError(f"Arrays have different shape prefixes: {shapes}")

