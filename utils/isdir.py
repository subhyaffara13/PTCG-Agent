
def isdir(path):
  if io_mode == BackendMode.DEFAULT:
    return os.path.isdir(path)
  elif io_mode == BackendMode.TF:
    return gfile.isdir(path)
  else:
    raise ValueError('Unknown IO Backend Mode.')

