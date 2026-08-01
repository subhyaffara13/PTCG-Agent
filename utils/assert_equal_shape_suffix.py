
def assert_equal_shape_suffix(inputs: Sequence[Array], suffix_len: int) -> None:
  """Checks that the final ``suffix_len`` dims of all inputs have same shape.

  Args:
    inputs: A collection of input arrays.
    suffix_len: A number of trailing dimensions to compare; each input's shape
      will be sliced to ``shape[-suffix_len:]``. Negative values are accepted
      and have the conventional Python indexing semantics.

  Raises:
    AssertionError: If the shapes of all arrays do not match.
    ValuleError: If ``inputs`` is not a collection of arrays.
  """
  _ai.assert_collection_of_arrays(inputs)

  shapes = [array.shape[-suffix_len:] for array in inputs]
  if shapes != [shapes[0]] * len(shapes):
    raise AssertionError(f"Arrays have different shape suffixes: {shapes}")

