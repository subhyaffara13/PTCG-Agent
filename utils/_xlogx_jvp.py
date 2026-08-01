
def _xlogx_jvp(primals, tangents):
  x, = primals
  x_dot, = tangents
  return  _xlogx(x), x_dot * (lax.log(x) + 1)

