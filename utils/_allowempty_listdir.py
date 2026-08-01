
def _allowempty_listdir(path: str):
  try:
    return io.listdir(path)
  except io.NotFoundError:
    return []

