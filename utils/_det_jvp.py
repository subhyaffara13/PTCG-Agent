
def _det_jvp(primals, tangents):
  x, = primals
  g, = tangents
  y, z = _cofactor_solve(x, g)
  return y, jnp.trace(z, axis1=-1, axis2=-2)

