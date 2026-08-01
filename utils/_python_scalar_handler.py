
def _python_scalar_handler(val, aval: core.AbstractValue | None):
  assert isinstance(aval, core.ShapedArray), aval
  assert aval.shape == (), aval
  return _numpy_array_constant(np.array(val, aval.dtype))

