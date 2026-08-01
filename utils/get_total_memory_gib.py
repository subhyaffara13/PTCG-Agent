
def get_total_memory_gib() -> float:
  if _profiler:
    return _profiler.total_memory_gib
  return 0.0

