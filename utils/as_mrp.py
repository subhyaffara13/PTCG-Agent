
def as_mrp(quat: Array) -> Array:
    xp = array_namespace(quat)
    one = xp.asarray(1.0, device=xp_device(quat), dtype=quat.dtype)
    sign = xp.where(quat[..., 3, None] < 0, -1, one)
    denominator = 1.0 + sign * quat[..., 3, None]
    return sign * quat[..., :3] / denominator

