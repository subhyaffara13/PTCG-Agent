
def assert_size(
    inputs: Union[Scalar, Union[Array, Sequence[Array]]],
    expected_sizes: Union[_ai.TShapeMatcher,
                          Sequence[_ai.TShapeMatcher]]) -> None:
  """Checks that the size of all inputs matches specified ``expected_sizes``.

  Valid usages include:

  .. code-block:: python

    assert_size(x, 1)                   # x is scalar (size 1)
    assert_size([x, y], (2, {1, 3}))    # x has size 2, y has size 1 or 3
    assert_size([x, y], (2, ...))       # x has size 2, y has any size
    assert_size([x, y], 1)              # x and y are scalar (size 1)
    assert_size((x, y), (5, 2))         # x has size 5, y has size 2

  Args:
    inputs: An array or a sequence of arrays.
    expected_sizes: A sqeuence of expected sizes associated with each input,
      where the expected size is a sequence of integer and `None` dimensions;
      if all inputs have same size, a single size may be passed as
      ``expected_sizes``.

  Raises:
    AssertionError: If the lengths of ``inputs`` and ``expected_sizes`` do not
      match; if ``expected_sizes`` has wrong type; if size of ``input`` does
      not match ``expected_sizes``.
  """
  # Ensure inputs and expected sizes are sequences.
  if not isinstance(inputs, collections.abc.Sequence):
    inputs = [inputs]

  if isinstance(expected_sizes, int):
    expected_sizes = [expected_sizes] * len(inputs)

  if not isinstance(expected_sizes, (list, tuple)):
    raise AssertionError(
        "Error in size compatibility check: expected sizes should be an int, "
        f"list, or tuple of ints, got {expected_sizes}.")

  if len(inputs) != len(expected_sizes):
    raise AssertionError(
        "Length of `inputs` and `expected_sizes` must match: "
        f"{len(inputs)} is not equal to {len(expected_sizes)}.")

  errors = []
  for idx, (x, expected) in enumerate(zip(inputs, expected_sizes)):
    size = getattr(x, "size", 1)  # scalars have size 1 by definition.
    # Allow any size for the ellipsis case and allow handling of integer
    # expected sizes or collection of acceptable expected sizes.
    int_condition = expected in {Ellipsis, None} or size == expected
    set_condition = (isinstance(expected, collections.abc.Collection) and
                     size in expected)
    if not (int_condition or set_condition):
      errors.append((idx, size, expected))

  if errors:
    msg = "; ".join(
        f"input {e[0]} has size {e[1]} but expected {e[2]}" for e in errors)
    raise AssertionError(f"Error in size compatibility check: {msg}.")

