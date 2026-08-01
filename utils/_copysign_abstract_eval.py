
def _copysign_abstract_eval(x1, x2):
  return jax_core.ShapedArray(x2.shape, x2.dtype)

