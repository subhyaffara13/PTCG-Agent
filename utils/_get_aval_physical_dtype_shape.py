
def _get_aval_physical_dtype_shape(aval):
  if should_physicalize_dtype(aval.dtype):
    physical_aval = _physical_aval(aval)
    return physical_aval.shape[len(aval.shape) :]
  else:
    return ()

