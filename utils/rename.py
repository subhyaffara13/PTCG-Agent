import os

def rename(src, dst, overwrite=False):
  if io_mode == BackendMode.DEFAULT:
    if os.path.exists(dst) and not overwrite:
      raise errors.AlreadyExistsError(dst)
    return os.rename(src, dst)
  elif io_mode == BackendMode.TF:
    return gfile.rename(src, dst, overwrite=overwrite)
  else:
    raise ValueError('Unknown IO Backend Mode.')

