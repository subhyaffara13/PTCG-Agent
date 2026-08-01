
def _jax_physical_dtype(dtype):
  # assuming () is a fine stand-in shape
  return _jax_physical_aval(core.ShapedArray((), dtype)).dtype

