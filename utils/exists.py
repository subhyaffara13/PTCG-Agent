
def exists(path):
  if io_mode == BackendMode.DEFAULT:
    return os.path.exists(path)
  elif io_mode == BackendMode.TF:
    return gfile.exists(path)
  else:
    raise ValueError('Unknown IO Backend Mode.')


def exists(path: str) -> bool:
    """Replacement for `os.path.exists` which works for host mapped volumes
    on Windows containers
    """
    try:
        os.lstat(path)
    except OSError:
        return False
    return True

