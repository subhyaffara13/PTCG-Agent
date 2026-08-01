
def maybe_import_libtpu():
  try:
    import libtpu  # pyrefly: ignore[missing-import]
  except ImportError:
    return None
  else:
    return libtpu

