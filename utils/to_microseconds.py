
def to_microseconds(duration: Duration) -> int:
  """Converts a Duration to microseconds."""
  return duration.ToMicroseconds()


def to_microseconds(ts: Timestamp) -> int:
  """Converts Timestamp to microseconds since epoch."""
  return ts.ToMicroseconds()

