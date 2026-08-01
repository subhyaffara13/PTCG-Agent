
def expi_jvp(primals, tangents):
  (x,) = primals
  (x_dot,) = tangents
  return expi(x), jnp.exp(x) / x * x_dot

