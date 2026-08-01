
def _parse_timedelta(val: str) -> datetime.timedelta:
  """Parses a duration string (e.g. '1s', '30m', '1h') into a timedelta."""
  if not isinstance(val, str):
    raise ValueError(
        f"Invalid duration type for client_keep_alive_interval: {type(val)},"
        " expected str."
    )
  seconds = pytimeparse.parse(val)
  if seconds is None:
    raise ValueError(
        f"Invalid duration format for client_keep_alive_interval: {val}"
    )
  return datetime.timedelta(seconds=seconds)

