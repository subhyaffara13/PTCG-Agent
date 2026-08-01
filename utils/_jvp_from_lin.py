
def _jvp_from_lin(f, primals, tangents):
  primal_out, f_lin = api.linearize(f, *primals)
  tangent_out = f_lin(*tangents)
  return primal_out, tangent_out

