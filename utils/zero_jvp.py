
def zero_jvp(primitive, primals, tangents, **params):
  r = primitive.bind(*primals, **params)
  return r, p2tz(r)

