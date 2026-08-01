
def from_dual_quat(dual_quat: Array, *, scalar_first: bool = False) -> Array:
    xp = array_namespace(dual_quat)

    if dual_quat.shape[-1] != 8:
        raise ValueError(
            f"Expected `dual_quat` to have shape (..., 8), got {dual_quat.shape}."
        )

    real_part = dual_quat[..., :4]
    dual_part = dual_quat[..., 4:]
    if scalar_first:
        real_part = xp.roll(real_part, -1, axis=-1)
        dual_part = xp.roll(dual_part, -1, axis=-1)

    real_part, dual_part = _normalize_dual_quaternion(real_part, dual_part)

    rot_quat = from_quat(real_part)

    translation = 2.0 * compose_quat(dual_part, quat_inv(rot_quat))[..., :3]
    matrix = _create_transformation_matrix(translation, quat_as_matrix(rot_quat))

    return matrix

