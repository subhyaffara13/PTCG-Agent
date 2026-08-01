
def get_expected_surge_gib() -> float:
  if _profiler:
    return _profiler.get_expected_surge_gib()
  return 0.0

