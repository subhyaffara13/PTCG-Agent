
def _python_scalar_attribute_handler(dtype, val):
  return _numpy_scalar_attribute(np.array(val, dtype))

