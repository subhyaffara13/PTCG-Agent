
def eval_bitcast_shape(x, dtype: DTypeLike):
  f = partial(bitcast, dtype=dtype)
  return api.eval_shape(f, api.ShapeDtypeStruct.like(x)).shape

