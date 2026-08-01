
def string_to_standard(level):
  """Converts a string level to standard logging level value.

  Args:
    level: str, case-insensitive ``'debug'``, ``'info'``, ``'warning'``,
        ``'error'``, ``'fatal'``.

  Returns:
    The corresponding integer level for use in standard logging.
  """
  return absl_to_standard(ABSL_NAMES.get(level.upper()))

