
def sici_jvp(primals, tangents):
  (p,), (t,) = primals, tangents
  primal_out = sici(p)

  sin_term = sinc(p / np.pi)
  cos_term = jnp.cos(p) / p

  tangent_out = (sin_term * t, cos_term * t)
  return primal_out, tangent_out

