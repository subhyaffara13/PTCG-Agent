
def c(val: int | float, ty):
  if isinstance(ty, ir.IntegerType) or isinstance(ty, ir.IndexType):
    if not isinstance(val, (int, np.integer)):
      raise TypeError(type(val))
    attr = ir.IntegerAttr.get(ty, val)
  elif isinstance(ty, ir.FloatType):
    attr = ir.FloatAttr.get(ty, val)
  elif isinstance(ty, ir.VectorType):
    return vector.broadcast(ty, c(val, ir.VectorType(ty).element_type))
  else:
    raise NotImplementedError(ty)
  return arith.constant(ty, attr)

