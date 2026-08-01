
def _magnitude(quat: Array) -> Array:
  return 2. * jnp.arctan2(_vector_norm(quat[:3]), jnp.abs(quat[3]))

