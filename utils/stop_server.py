
def stop_server():
  """Stops the running profiler server."""
  global _profiler_server
  if _profiler_server is None:
    raise ValueError("No active profiler server.")
  _profiler_server = None # Should destroy the profiler server

