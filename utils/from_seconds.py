
def from_seconds(seconds: float) -> Duration:
  """Converts seconds to Duration."""
  duration = Duration()
  duration.FromSeconds(seconds)
  return duration


def from_seconds(seconds: float) -> Timestamp:
  """Converts seconds since epoch to Timestamp."""
  timestamp = Timestamp()
  timestamp.FromSeconds(seconds)
  return timestamp

