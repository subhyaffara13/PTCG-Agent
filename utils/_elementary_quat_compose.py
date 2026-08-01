
def _elementary_quat_compose(axes: list[int], angles: Array, intrinsic: bool) -> Array:
    xp = array_namespace(angles)
    device = xp_device(angles)
    quat = _make_elementary_quat(axes[0], angles[..., 0], device=device, xp=xp)
    for i in range(1, len(axes)):
        ax_quat = _make_elementary_quat(axes[i], angles[..., i], device=device, xp=xp)
        quat = compose_quat(quat, ax_quat) if intrinsic else compose_quat(ax_quat, quat)
    return quat


def _elementary_quat_compose(angles: Array, axes: Array, intrinsic: bool, degrees: bool) -> Array:
  angles = jnp.where(degrees, jnp.deg2rad(angles), angles)
  result = _make_elementary_quat(axes[0], angles[0])
  for idx in range(1, len(axes)):
    quat = _make_elementary_quat(axes[idx], angles[idx])
    result = jnp.where(intrinsic, _compose_quat(result, quat), _compose_quat(quat, result))
  return result

