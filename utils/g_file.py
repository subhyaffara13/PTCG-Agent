
def GFile(name, mode):  # pylint: disable=invalid-name
  if io_mode == BackendMode.DEFAULT:
    if 'b' in mode:
      return open(name, mode)  # pylint: disable=unspecified-encoding
    else:
      return open(name, mode, encoding='utf-8')
  elif io_mode == BackendMode.TF:
    return gfile.GFile(name, mode)
  else:
    raise ValueError('Unknown IO Backend Mode.')

