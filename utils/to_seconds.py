
def to_seconds(time_unit: time_unit_type) -> float:
    return float(
        time_unit.total_seconds() if isinstance(time_unit, timedelta) else time_unit
    )


def to_seconds(value: datetime | float | int | str | None) -> float | None:
    """Coerce a datetime / epoch / formatted-string value to epoch seconds."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.timestamp()
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(value, fmt).timestamp()
            except ValueError:
                continue
    return None


def to_seconds(duration: Duration) -> int:
  """Converts a Duration to seconds."""
  return duration.ToSeconds()


def to_seconds(ts: Timestamp) -> int:
  """Converts Timestamp to seconds since epoch."""
  return ts.ToSeconds()

