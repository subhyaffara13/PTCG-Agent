
def linear_jvp(primitive, primals, tangents, **params):
  val_out = primitive.bind(*primals, **params)
  if all(type(tangent) is Zero for tangent in tangents):
    if primitive.multiple_results:
      return val_out, map(p2tz, val_out)
    return val_out, p2tz(val_out)
  else:
    tangents = map(instantiate_zeros, tangents)
    return val_out, primitive.bind(*tangents, **params)

