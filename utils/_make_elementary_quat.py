
def _make_elementary_quat(axis: int, angle: Array, device, xp) -> Array:
    quat = xp.zeros((*angle.shape, 4), dtype=angle.dtype, device=device)
    quat = xpx.at(quat)[..., 3].set(xp.cos(angle / 2.0))
    quat = xpx.at(quat)[..., axis].set(xp.sin(angle / 2.0))
    return quat


def _make_elementary_quat(axis: int, angle: Array) -> Array:
  quat = jnp.zeros(4, dtype=angle.dtype)
  quat = quat.at[3].set(jnp.cos(angle / 2.))
  quat = quat.at[axis].set(jnp.sin(angle / 2.))
  return quat

