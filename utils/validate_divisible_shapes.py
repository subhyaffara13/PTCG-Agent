
def validate_divisible_shapes(
    divided_shape: Shape,
    dividing_shape: Shape,
) -> bool:
  """Returns True only if dividing_shape is a divisor of divided_shape."""
  try:
    return not np.mod(divided_shape, dividing_shape).any()
  except ValueError:
    # eg. imcompatible shape
    return False

