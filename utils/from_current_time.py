
def from_current_time() -> Timestamp:
  """Converts the current UTC to Timestamp."""
  timestamp = Timestamp()
  timestamp.FromDatetime(datetime.datetime.now(tz=datetime.timezone.utc))
  return timestamp

