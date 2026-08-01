
def _to_jax_shape(s):
  return core.ShapedArray(s.dimensions(), s.numpy_dtype())

