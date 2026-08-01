
def _broadcast_to_abstract_eval(aval, *, shape):
  return core.ShapedArray(shape, aval.dtype)

