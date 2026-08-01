
def _check_special(name: str, dtype: np.dtype, buf: basearray.Array) -> None:
  if dtypes.issubdtype(dtype, np.inexact):
    if config.debug_nans.value and np.any(np.isnan(np.asarray(buf))):
      raise InternalFloatingPointError(name, "nan")
    if config.debug_infs.value and np.any(np.isinf(np.asarray(buf))):
      raise InternalFloatingPointError(name, "inf")

