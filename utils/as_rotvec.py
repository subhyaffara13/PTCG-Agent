
def as_rotvec(quat: Array, degrees: bool = False) -> Array:
    xp = array_namespace(quat)
    quat = _quat_canonical(quat)
    ax_norm = xp_vector_norm(quat[..., :3], axis=-1, keepdims=True, xp=xp)
    angle = 2 * xp.atan2(ax_norm, quat[..., 3][..., None])
    small_angle = angle <= 1e-3
    angle2 = angle**2
    small_scale = 2 + angle2 / 12 + 7 * angle2**2 / 2880
    # We need to handle the case where sin(angle/2) is 0 to avoid division by zero. We
    # use the value of the Taylor series approximation, but non-branching operations
    # require that we still divide by the sin. Since we do not use the result where the
    # angle is close to 0, adding one to the sin where we discard the result is safe.
    div_sin = xp.sin(angle / 2.0) + xp.asarray(small_angle, dtype=angle.dtype)
    large_scale = angle / div_sin
    scale = xp.where(small_angle, small_scale, large_scale)
    if degrees:
        scale = _rad2deg(scale)
    rotvec = scale * quat[..., :3]
    return rotvec

