
def _reduce_prod_jvp_rule(primals, tangents, *, axes):
  reducer = lambda x, y: [mul(x, y)]
  primals_out, tangents_out = _reduce_jvp(reducer, [_const(primals[0], 1)],
                                          primals, tangents, axes)
  return primals_out[0], tangents_out[0]

