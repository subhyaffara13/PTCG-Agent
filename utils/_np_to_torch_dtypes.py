
def _np_to_torch_dtypes() -> dict[np.dtype, torch_.dtype]:
  """Returns mapping numpy -> torch dtypes."""
  return dict((np.dtype(n), t) for t, n in _torch_to_np_dtypes().items())

