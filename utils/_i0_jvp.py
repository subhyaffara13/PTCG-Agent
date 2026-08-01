
def _i0_jvp(primals, tangents):
  primal_out, tangent_out = api.jvp(_i0.fun, primals, tangents)
  return primal_out, where(primals[0] == 0, 0.0, tangent_out)

