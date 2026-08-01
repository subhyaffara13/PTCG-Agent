
def _precise_dot(A: ArrayLike, B: ArrayLike) -> Array:
  return jnp.dot(A, B, precision=lax.Precision.HIGHEST)

