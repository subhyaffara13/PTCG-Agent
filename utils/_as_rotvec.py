
def _as_rotvec(quat: Array, degrees: bool) -> Array:
  quat = jnp.where(quat[3] < 0, -quat, quat)  # w > 0 to ensure 0 <= angle <= pi
  angle = 2. * jnp.arctan2(_vector_norm(quat[:3]), quat[3])
  angle2 = angle * angle
  small_scale = 2 + angle2 / 12 + 7 * angle2 * angle2 / 2880
  large_scale = angle / jnp.sin(angle / 2)
  scale = jnp.where(angle <= 1e-3, small_scale, large_scale)
  scale = jnp.where(degrees, jnp.rad2deg(scale), scale)
  return scale * jnp.array(quat[:3])

