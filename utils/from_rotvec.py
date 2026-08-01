
def from_rotvec(rotvec: Array, degrees: bool = False) -> Array:
    xp = array_namespace(rotvec)
    if rotvec.shape[-1] != 3:
        raise ValueError(
            f"Expected `rot_vec` to have shape (..., 3), got {rotvec.shape}"
        )
    rotvec = _deg2rad(rotvec) if degrees else rotvec

    angle = xp_vector_norm(rotvec, axis=-1, keepdims=True, xp=xp)
    small_angle = angle <= 1e-3
    angle2 = angle**2
    small_scale = 0.5 - angle2 / 48 + angle2**2 / 3840
    # We need to handle the case where angle is 0 to avoid division by zero. We use the
    # value of the Taylor series approximation, but non-branching operations require
    # that we still divide by the angle. Since we do not use the result where the angle
    # is close to 0, this is safe.
    div_angle = angle + xp.asarray(small_angle, dtype=angle.dtype)
    large_scale = xp.sin(angle / 2) / div_angle
    scale = xp.where(small_angle, small_scale, large_scale)
    quat = xp.concat([rotvec * scale, xp.cos(angle / 2)], axis=-1)
    return quat

