
def _to_shape_dtype(x):
  if isinstance(x, Variable):
    value = x.get_raw_value()
    metadata = x.get_metadata()
    value = jax.tree.map(_to_shape_dtype, value)
    return VariableRepr(x.var_type, value, metadata)
  elif variablelib.is_array_ref(x) and np.prod(x.shape) > 1:
    return MutableArrayRepr(x.shape, x.dtype)
  elif (
    isinstance(x, (np.ndarray, jax.Array))
    and np.prod(x.shape) > 1
  ):
    return ArrayRepr(x.shape, x.dtype)
  return x

