
def from_milliseconds(millis: float) -> Duration:
  """Converts milliseconds to Duration."""
  duration = Duration()
  duration.FromMilliseconds(millis)
  return duration


def from_milliseconds(millis: float) -> Timestamp:
  """Converts milliseconds since epoch to Timestamp."""
  timestamp = Timestamp()
  timestamp.FromMilliseconds(millis)
  return timestamp

