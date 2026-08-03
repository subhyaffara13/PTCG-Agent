import os

def listdir(path):
  if io_mode == BackendMode.DEFAULT:
    return os.listdir(path=path)
  elif io_mode == BackendMode.TF:
    return gfile.listdir(path=path)
  else:
    raise ValueError('Unknown IO Backend Mode.')

