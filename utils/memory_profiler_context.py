
def memory_profiler_context():
  """Context manager for memory_regulator profiler."""
  memory_regulator.profiler_start()
  try:
    yield
  finally:
    # Explicitly stop the bg thread if an exception occurs
    memory_regulator.profiler_end()

