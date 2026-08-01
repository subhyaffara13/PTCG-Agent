
def to_milliseconds(duration: Duration) -> int:
  """Converts a Duration to milliseconds."""
  return duration.ToMilliseconds()


def to_milliseconds(ts: Timestamp) -> int:
  """Converts Timestamp to milliseconds since epoch."""
  return ts.ToMilliseconds()

