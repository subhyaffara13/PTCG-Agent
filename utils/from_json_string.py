
def from_json_string(value: str) -> Duration:
  """Converts a string to Duration.

  Args:
    value: A string to be converted. The string must end with 's'. Any
      fractional digits (or none) are accepted as long as they fit into
      precision. For example: "1s", "1.01s", "1.0000001s", "-3.100s"

  Raises:
    ValueError: On parsing problems.
  """
  duration = Duration()
  duration.FromJsonString(value)
  return duration


def from_json_string(value: str) -> Timestamp:
  """Parse a RFC 3339 date string format to Timestamp.

  Args:
    value: A date string. Any fractional digits (or none) and any offset are
      accepted as long as they fit into nano-seconds precision. Example of
      accepted format: '1972-01-01T10:00:20.021-05:00'

  Raises:
    ValueError: On parsing problems.
  """
  timestamp = Timestamp()
  timestamp.FromJsonString(value)
  return timestamp

