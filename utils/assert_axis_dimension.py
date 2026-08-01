
def assert_axis_dimension(tensor: Array, axis: int, expected: int) -> None:
  """Checks that ``tensor.shape[axis] == expected``.

  Args:
    tensor: A JAX array.
    axis: An integer specifying which axis to assert.
    expected: An expected value of ``tensor.shape[axis]``.

  Raises:
    AssertionError:
      The dimension of the specified axis does not match the prescribed value.
  """
  assert_axis_dimension_comparator(
      tensor,
      axis,
      pass_fn=lambda tensor_dim: tensor_dim == expected,
      error_string=f"equal to '{expected}'")

