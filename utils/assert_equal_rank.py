
def assert_equal_rank(inputs: Sequence[Array]) -> None:
  """Checks that all arrays have the same rank.

  Args:
    inputs: A collection of arrays.

  Raises:
    AssertionError: If the ranks of all arrays do not match.
    ValueError: If ``inputs`` is not a collection of arrays.
  """
  _ai.assert_collection_of_arrays(inputs)

  rank = len(inputs[0].shape)
  expected_ranks = [rank] * len(inputs)
  ranks = [len(x.shape) for x in inputs]
  if ranks != expected_ranks:
    raise AssertionError(f"Arrays have different rank: {ranks}.")

