
def from_nanoseconds(nanos: float) -> Duration:
  """Converts nanoseconds to Duration."""
  duration = Duration()
  duration.FromNanoseconds(nanos)
  return duration


def from_nanoseconds(nanos: float) -> Timestamp:
  """Converts nanoseconds since epoch to Timestamp."""
  timestamp = Timestamp()
  timestamp.FromNanoseconds(nanos)
  return timestamp

