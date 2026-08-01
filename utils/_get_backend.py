
def _get_backend(xp):
    if is_numpy(xp):
        return _rbfinterp_np
    return _rbfinterp_xp


def _get_backend(p0: _GPath, p1: _GPath) -> backend_lib.Backend:
  """When composing with another backend, GCS win.

  To allow `Path('.').replace('gs://')`

  Args:
    p0: Path to compare
    p1: Path to compare

  Returns:
    GCS backend if one of the 2 path is GCS, else p0 backend.
  """
  # pylint: disable=protected-access
  if p0._backend in _GCS_BACKENDS:
    return p0._backend
  elif p1._backend in _GCS_BACKENDS:
    return p1._backend
  else:
    return p0._backend

