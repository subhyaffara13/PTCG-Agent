
def makedirs(path):
  if io_mode == BackendMode.DEFAULT:
    return os.makedirs(path, exist_ok=True)
  elif io_mode == BackendMode.TF:
    return gfile.makedirs(path)
  else:
    raise ValueError('Unknown IO Backend Mode.')

