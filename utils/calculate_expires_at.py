
def calculate_expires_at(
    interval: datetime.timedelta,
    grace_ratio: float = 0.2,
) -> datetime.datetime:
  """Calculates a new expiration timestamp with a grace period buffer.

  The grace period acts as a buffer to account for communication delay.

  Args:
    interval: The base timeout interval.
    grace_ratio: Optional ratio of the interval to use as a grace buffer
      (default is 0.2).

  Returns:
    The calculated expiration datetime in UTC.
  """
  grace_buffer = interval * grace_ratio
  total_interval = interval + grace_buffer
  return datetime.datetime.now(datetime.timezone.utc) + total_interval

