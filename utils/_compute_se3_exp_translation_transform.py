
def _compute_se3_exp_translation_transform(rot_vec: Array) -> Array:
    """Compute the transformation matrix from the se3 translation part to SE3
    translation.

    The transformation matrix depends on the rotation vector.
    """
    xp = array_namespace(rot_vec)
    device = xp_device(rot_vec)
    dtype = rot_vec.dtype
    angle = xp_vector_norm(rot_vec, axis=-1, keepdims=True, xp=xp)
    small_scale = angle < 1e-3

    k1_small = 0.5 - angle**2 / 24 + angle**4 / 720
    # Avoid division by zero for non-branching computations. The value will get
    # discarded in the xp.where selection.
    safe_angle = angle + xp.asarray(small_scale, dtype=dtype, device=device)
    k1 = (1.0 - xp.cos(angle)) / safe_angle**2
    k1 = xp.where(small_scale, k1_small, k1)

    k2_small = 1 / 6 - angle**2 / 120 + angle**4 / 5040
    # Again, avoid division by zero by adding one to all near-zero angles.
    safe_angle = angle + xp.asarray(small_scale, dtype=dtype, device=device)
    k2 = (angle - xp.sin(angle)) / safe_angle**3
    k2 = xp.where(small_scale, k2_small, k2)

    s = _create_skew_matrix(rot_vec)
    eye = xp.eye(3, dtype=dtype, device=device)

    return eye + k1[..., None] * s + k2[..., None] * s @ s

