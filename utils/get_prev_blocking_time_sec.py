
def get_prev_blocking_time_sec() -> float:
  if _profiler:
    return _profiler.get_prev_blocking_time_sec()
  return 0.0

