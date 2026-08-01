
def standard_jvp2(jvprules, primitive, primals, tangents, **params):
  val_out = primitive.bind(*primals, **params)
  tangents_out = (rule(t, val_out, *primals, **params) for rule, t in zip(jvprules, tangents)
                  if rule is not None and type(t) is not Zero)
  tangents_out = list(tangents_out)
  return val_out, functools.reduce(add_tangents, tangents_out, p2tz(val_out))

