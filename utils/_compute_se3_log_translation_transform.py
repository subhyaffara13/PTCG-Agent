
def _compute_se3_log_translation_transform(rot_vec: Array) -> Array:
    """Compute the transformation matrix from SE3 translation to the se3
    translation part.

    It is the inverse of `_compute_se3_exp_translation_transform` in a closed
    analytical form.
    """
    xp = array_namespace(rot_vec)
    dtype = rot_vec.dtype
    device = xp_device(rot_vec)
    angle = xp_vector_norm(rot_vec, axis=-1, keepdims=True, xp=xp)
    mask = angle < 1e-3

    k_small = 1 / 12 + angle**2 / 720 + angle**4 / 30240
    safe_angle = angle + xp.asarray(mask, dtype=dtype, device=device)
    k = (1 - 0.5 * angle / xp.tan(0.5 * safe_angle)) / safe_angle**2
    k = xp.where(mask, k_small, k)

    s = _create_skew_matrix(rot_vec)

    return xp.eye(3, dtype=dtype, device=device) - 0.5 * s + k[..., None] * s @ s

