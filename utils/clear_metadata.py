
def clear_metadata() -> None:
  """Clears metadata for the current profiling session."""
  if hasattr(_profiler, "clear_metadata"):
    return _profiler.clear_metadata()

