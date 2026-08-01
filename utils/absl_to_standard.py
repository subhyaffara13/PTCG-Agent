
def absl_to_standard(level):
  """Converts an integer level from the absl value to the standard value.

  Args:
    level: int, an absl.logging level.

  Raises:
    TypeError: Raised when level is not an integer.

  Returns:
    The corresponding integer level for use in standard logging.
  """
  if not isinstance(level, int):
    raise TypeError(f'Expect an int level, found {type(level)}')
  if level < ABSL_FATAL:
    level = ABSL_FATAL
  if level <= ABSL_DEBUG:
    return ABSL_TO_STANDARD[level]
  # Maps to vlog levels.
  return STANDARD_DEBUG - level + 1

