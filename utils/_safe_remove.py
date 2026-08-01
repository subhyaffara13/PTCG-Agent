
def _safe_remove(path: str):
  """Identify whether a path is a dir or list and choose the correct remove method."""
  if io.isdir(path):
    io.rmtree(path)
  else:
    io.remove(path)

