
def _mm(a, b, precision=jax.lax.Precision.HIGHEST):
  return jax.lax.dot(a, b, precision=(precision, precision))

