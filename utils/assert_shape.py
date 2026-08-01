
def assert_shape(
    inputs: Union[Scalar, Union[Array, Sequence[Array]]],
    expected_shapes: Union[_ai.TShapeMatcher,
                           Sequence[_ai.TShapeMatcher]]) -> None:
  """Checks that the shape of all inputs matches specified ``expected_shapes``.

  Valid usages include:

  .. code-block:: python

    assert_shape(x, ())                  # x is scalar
    assert_shape(x, (2, 3))              # x has shape (2, 3)
    assert_shape(x, (2, {1, 3}))         # x has shape (2, 1) or (2, 3)
    assert_shape(x, (2, None))           # x has rank 2 and `x.shape[0] == 2`
    assert_shape(x, (2, ...))            # x has rank >= 1 and `x.shape[0] == 2`
    assert_shape([x, y], ())             # x and y are scalar
    assert_shape([x, y], [(), (2,3)])    # x is scalar and y has shape (2, 3)

  Args:
    inputs: An array or a sequence of arrays.
    expected_shapes: A sequence of expected shapes associated with each input,
      where the expected shape is a sequence of integer and `None` dimensions;
      if all inputs have same shape, a single shape may be passed as
      ``expected_shapes``.

  Raises:
    AssertionError: If the lengths of ``inputs`` and ``expected_shapes`` do not
      match; if ``expected_shapes`` has wrong type; if shape of ``input`` does
      not match ``expected_shapes``.
  """
  if not isinstance(expected_shapes, (list, tuple)):
    raise AssertionError(
        "Error in shape compatibility check: expected shapes should be a list "
        f"or tuple of ints, got {expected_shapes}.")

  # Ensure inputs and expected shapes are sequences.
  if not isinstance(inputs, collections.abc.Sequence):
    inputs = [inputs]

  # Shapes are always lists or tuples, not scalars.
  if (not expected_shapes or not isinstance(expected_shapes[0], (list, tuple))):
    expected_shapes = [expected_shapes] * len(inputs)
  if len(inputs) != len(expected_shapes):
    raise AssertionError(
        "Length of `inputs` and `expected_shapes` must match: "
        f"{len(inputs)} is not equal to {len(expected_shapes)}.")

  errors = []
  for idx, (x, expected) in enumerate(zip(inputs, expected_shapes)):
    shape = getattr(x, "shape", ())  # scalars have shape () by definition.
    if not _shape_matches(shape, expected):
      errors.append((idx, shape, _ai.format_shape_matcher(expected)))

  if errors:
    msg = "; ".join(
        f"input {e[0]} has shape {e[1]} but expected {e[2]}" for e in errors)
    raise AssertionError(f"Error in shape compatibility check: {msg}.")

