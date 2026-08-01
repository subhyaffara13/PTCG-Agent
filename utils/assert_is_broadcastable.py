
def assert_is_broadcastable(shape_a: Sequence[int],
                            shape_b: Sequence[int]) -> None:
  """Checks that an array of ``shape_a`` is broadcastable to one of ``shape_b``.

  Args:
    shape_a: A shape of the array to check.
    shape_b: A target shape after broadcasting.

  Raises:
    AssertionError: If ``shape_a`` is not broadcastable to ``shape_b``.
  """
  error = AssertionError(
      f"Shape {shape_a} is not broadcastable to shape {shape_b}.")
  ndim_a = len(shape_a)
  ndim_b = len(shape_b)
  if ndim_a > ndim_b:
    raise error
  else:
    for i in range(1, ndim_a + 1):
      if shape_a[-i] != 1 and shape_a[-i] != shape_b[-i]:
        raise error

