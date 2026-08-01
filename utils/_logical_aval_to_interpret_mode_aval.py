
def _logical_aval_to_interpret_mode_aval(aval):
  if isinstance(aval, state.AbstractRef):
    inner_aval = _logical_aval_to_interpret_mode_aval(aval.inner_aval)
    return aval.update(inner_aval=inner_aval)
  if isinstance(aval, jax_core.ShapedArray):
    inner_dtype = _logical_to_interpret_mode_dtype(aval.dtype)
    return jax_core.ShapedArray(aval.shape, inner_dtype, weak_type=aval.weak_type)
  return aval

