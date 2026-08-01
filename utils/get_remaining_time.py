
def get_remaining_time(
    start_time: float, timeout_secs: Optional[float]
) -> Optional[float]:
  """Returns remaining time in secs, or None if timeout_secs is None."""
  if timeout_secs is None:
    return None
  elapsed = time.time() - start_time
  if elapsed >= timeout_secs:
    raise TimeoutError(f'Timed out after {elapsed} seconds.')
  return timeout_secs - elapsed

