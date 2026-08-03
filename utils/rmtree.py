import sys

def rmtree(path):
  """Remove a directory and recursively all contents inside. Might fail if used on a file path."""
  if io_mode == BackendMode.DEFAULT:
    return shutil.rmtree(path)
  elif io_mode == BackendMode.TF:
    return gfile.rmtree(path)
  else:
    raise ValueError('Unknown IO Backend Mode.')


def rmtree(path, ignore_errors=False, onexc=_auto_chmod):
    """
    Similar to ``shutil.rmtree`` but automatically executes ``chmod``
    for well know Windows failure scenarios.
    """
    return py311.shutil_rmtree(path, ignore_errors, onexc)


def rmtree(dir: str, ignore_errors: bool = False, onexc: OnExc | None = None) -> None:
    if ignore_errors:
        onexc = _onerror_ignore
    if onexc is None:
        onexc = _onerror_reraise
    handler: OnErr = partial(rmtree_errorhandler, onexc=onexc)
    if sys.version_info >= (3, 12):
        # See https://docs.python.org/3.12/whatsnew/3.12.html#shutil.
        shutil.rmtree(dir, onexc=handler)  # type: ignore
    else:
        shutil.rmtree(dir, onerror=handler)  # type: ignore


def rmtree(path: epath.Path) -> None:
  """Deletes a GCS path, performing HNS folder cleanup if necessary.

  Args:
    path: the global path to delete, must be a GCS path.

  Raises:
    ValueError: if path is not a GCS path.
  """
  if not is_gcs_path(path):
    raise ValueError(f'Path is not a GCS path: {path}')

  path.rmtree()

  # For HNS, clean up the remaining empty directory structure.
  if is_hierarchical_namespace_enabled(path):
    cleanup_hns_folders(path)

