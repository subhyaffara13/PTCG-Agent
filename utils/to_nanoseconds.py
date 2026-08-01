
def to_nanoseconds(duration: Duration) -> int:
  """Converts a Duration to nanoseconds."""
  return duration.ToNanoseconds()


def to_nanoseconds(ts: Timestamp) -> int:
  """Converts Timestamp to nanoseconds since epoch."""
  return ts.ToNanoseconds()

