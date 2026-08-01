
def _nsecs_to_datetime(nsecs: int | None) -> datetime.datetime | None:
  if nsecs is None:
    return None
  return datetime.datetime.fromtimestamp(nsecs / 1e9, tz=datetime.timezone.utc)

