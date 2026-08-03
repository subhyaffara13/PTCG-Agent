from typing import Set, Union

def assert_rank(
    inputs: Union[Scalar, Union[Array, Sequence[Array]]],
    expected_ranks: Union[int, Set[int], Sequence[Union[int,
                                                        Set[int]]]]) -> None:
  """Checks that the rank of all inputs matches specified ``expected_ranks``.

  Valid usages include:

  .. code-block:: python

    assert_rank(x, 0)                      # x is scalar
    assert_rank(x, 2)                      # x is a rank-2 array
    assert_rank(x, {0, 2})                 # x is scalar or rank-2 array
    assert_rank([x, y], 2)                 # x and y are rank-2 arrays
    assert_rank([x, y], [0, 2])            # x is scalar and y is a rank-2 array
    assert_rank([x, y], {0, 2})            # x and y are scalar or rank-2 arrays

  Args:
    inputs: An array or a sequence of arrays.
    expected_ranks: A sequence of expected ranks associated with each input,
      where the expected rank is either an integer or set of integer options; if
      all inputs have same rank, a single scalar or set of scalars may be passed
      as ``expected_ranks``.

  Raises:
    AssertionError: If lengths of ``inputs`` and ``expected_ranks`` don't match;
      if ``expected_ranks`` has wrong type;
      if the ranks of ``inputs`` do not match ``expected_ranks``.
    ValueError: If ``expected_ranks`` is not an integer and not a sequence of
     integets.
  """
  if not isinstance(expected_ranks, (collections.abc.Collection, int)):
    raise ValueError(
        f"Error in rank compatibility check: expected ranks should be a single "
        f"integer or a collection of integers, got {expected_ranks}.")

  if isinstance(expected_ranks, np.ndarray):  # ndarray is abc.Collection
    raise ValueError(
        f"Error in rank compatibility check: expected ranks should be a single "
        f"integer or a collection of integers, but was an array: "
        f"{expected_ranks}.")

  # Ensure inputs and expected ranks are sequences.
  if not isinstance(inputs, collections.abc.Sequence):
    inputs = [inputs]
  if (not isinstance(expected_ranks, collections.abc.Sequence) or
      isinstance(expected_ranks, collections.abc.Set)):
    expected_ranks = [expected_ranks] * len(inputs)
  if len(inputs) != len(expected_ranks):
    raise AssertionError(
        "Length of inputs and expected_ranks must match: inputs has length "
        f"{len(inputs)}, expected_ranks has length {len(expected_ranks)}.")

  errors = []
  for idx, (x, expected) in enumerate(zip(inputs, expected_ranks)):
    if hasattr(x, "shape"):
      shape = x.shape
    else:
      shape = ()  # scalars have shape () by definition.
    rank = len(shape)

    # Multiple expected options can be specified.

    # Check against old usage where options could be any sequence
    if (isinstance(expected, collections.abc.Sequence) and
        not isinstance(expected, collections.abc.Set)):
      raise ValueError("Error in rank compatibility check: "
                       "Expected ranks should be integers or sets of integers.")

    options = (
        expected if isinstance(expected, collections.abc.Set) else {expected})

    if rank not in options:
      errors.append((idx, rank, shape, expected))

  if errors:
    msg = "; ".join(
        f"input {e[0]} has rank {e[1]} (shape {e[2]}) but expected {e[3]}"
        for e in errors)

    raise AssertionError(f"Error in rank compatibility check: {msg}.")

