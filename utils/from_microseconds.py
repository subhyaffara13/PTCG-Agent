
def from_microseconds(micros: float) -> Duration:
  """Converts microseconds to Duration."""
  duration = Duration()
  duration.FromMicroseconds(micros)
  return duration


def from_microseconds(micros: float) -> Timestamp:
  """Converts microseconds since epoch to Timestamp."""
  timestamp = Timestamp()
  timestamp.FromMicroseconds(micros)
  return timestamp

