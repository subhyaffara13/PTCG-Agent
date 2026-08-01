
def _normalize_dual_quaternion(
    real_part: Array, dual_part: Array
) -> tuple[Array, Array]:
    """Ensure that the dual quaternion has unit norm.

    The norm is a dual number and must be 1 + 0 * epsilon, which means that
    the real quaternion must have unit norm and the dual quaternion must be
    orthogonal to the real quaternion.
    """
    xp = array_namespace(real_part)

    real_norm = xp_vector_norm(real_part, axis=-1, keepdims=True, xp=xp)

    # special case: real quaternion is 0, we set it to identity
    zero_real_mask = real_norm == 0.0
    unit_quat = xp.asarray(
        [0.0, 0.0, 0.0, 1.0], dtype=real_part.dtype, device=xp_device(real_part)
    )
    real_part = xp.where(zero_real_mask, unit_quat, real_part)
    real_norm = xp.where(zero_real_mask, 1.0, real_norm)

    # 1. ensure unit real quaternion
    real_part = real_part / real_norm
    dual_part = dual_part / real_norm

    # 2. ensure orthogonality of real and dual quaternion
    dual_part -= xp.sum(real_part * dual_part, axis=-1, keepdims=True) * real_part

    return real_part, dual_part

