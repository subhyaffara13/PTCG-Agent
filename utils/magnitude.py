
def magnitude(quat: Array) -> Array:
    xp = array_namespace(quat)
    sin_q = xp_vector_norm(quat[..., :3], axis=-1, xp=xp)
    cos_q = xp.abs(quat[..., 3])
    angles = 2 * xp.atan2(sin_q, cos_q)
    return angles

