
def _from_rotvec(rotvec: Array, degrees: bool) -> Array:
  rotvec = jnp.where(degrees, jnp.deg2rad(rotvec), rotvec)
  angle = _vector_norm(rotvec)
  angle2 = angle * angle
  small_scale = scale = 0.5 - angle2 / 48 + angle2 * angle2 / 3840
  large_scale = jnp.sin(angle / 2) / angle
  scale = jnp.where(angle <= 1e-3, small_scale, large_scale)
  return jnp.hstack([scale * rotvec, jnp.cos(angle / 2)])

