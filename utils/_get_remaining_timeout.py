
def _get_remaining_timeout(
    start_time: float,
    timeout_secs: float,
    error_message: str,
) -> float:
  """Returns remaining timeout in seconds, or raises TimeoutError if expired."""
  time_remaining = timeout_secs - (time.time() - start_time)
  if time_remaining <= 0:
    raise TimeoutError(error_message)
  return time_remaining

