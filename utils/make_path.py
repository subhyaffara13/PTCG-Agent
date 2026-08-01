
def make_path(path: PathLike) -> abstract_path.Path:
  """Create a generic `pathlib.Path`-like abstraction.

  Depending on the input (e.g. `gs://`, `github://`, `ResourcePath`,...), the
  system (Windows, Linux,...), the function will create the right pathlib-like
  abstraction.

  Args:
    path: Pathlike object.

  Returns:
    path: The `pathlib.Path`-like abstraction.
  """
  is_windows = os.name == 'nt'
  if isinstance(path, str):
    uri_splits = path.split('://', maxsplit=1)
    if len(uri_splits) > 1:  # str is URI (e.g. `gs://`, `github://`,...)
      # On windows, `PosixGPath` is created for `gs://` paths
      return _URI_PREFIXES_TO_CLS[uri_splits[0] + '://'](path)  # pytype: disable=bad-return-type
    elif is_windows:
      return gpath.WindowsGPath(path)
    else:
      return gpath.PosixGPath(path)
  elif isinstance(path, _PATHLIKE_CLS):
    return path  # Forward resource path, gpath,... as-is  # pytype: disable=bad-return-type
  elif isinstance(path, os.PathLike):  # Other `os.fspath` compatible objects
    path_cls = gpath.WindowsGPath if is_windows else gpath.PosixGPath
    return path_cls(path)
  else:
    raise TypeError(f'Invalid path type: {path!r}')

