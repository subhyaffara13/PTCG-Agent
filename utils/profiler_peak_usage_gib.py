
def profiler_peak_usage_gib() -> float:
  if _profiler:
    return _profiler.peak_usage_gib
  return 0.0

