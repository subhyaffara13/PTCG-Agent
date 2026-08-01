
def from_timedelta(td: datetime.timedelta) -> Duration:
  """Converts timedelta to Duration."""
  duration = Duration()
  duration.FromTimedelta(td)
  return duration

