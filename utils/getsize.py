import os

def getsize(path):
  """Return the size, in bytes, of path."""
  if io_mode == BackendMode.DEFAULT:
    return os.path.getsize(path)
  elif io_mode == BackendMode.TF:
    return gfile.stat(path).length
  else:
    raise ValueError('Unknown IO Backend Mode.')

