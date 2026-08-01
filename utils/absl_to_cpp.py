
def absl_to_cpp(level):
  """Converts an absl log level to a cpp log level.

  Args:
    level: int, an absl.logging level.

  Raises:
    TypeError: Raised when level is not an integer.

  Returns:
    The corresponding integer level for use in Abseil C++.
  """
  if not isinstance(level, int):
    raise TypeError(f'Expect an int level, found {type(level)}')
  if level >= 0:
    # C++ log levels must be >= 0
    return 0
  else:
    return -level

