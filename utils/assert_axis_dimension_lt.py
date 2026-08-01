
def assert_axis_dimension_lt(tensor: Array, axis: int, val: int) -> None:
  """Checks that ``tensor.shape[axis] < val``.

  Args:
    tensor: A JAX Array.
    axis: An integer specifiying which axis to assert.
    val: A value ``tensor.shape[axis]`` must be less than.

  Raises:
    AssertionError: if the dimension of ``axis`` is >= ``val``.
  """
  assert_axis_dimension_comparator(
      tensor,
      axis,
      pass_fn=lambda tensor_dim: tensor_dim < val,
      error_string=f"less than '{val}'")

