
def as_dual_quat(matrix: Array, *, scalar_first: bool = False) -> Array:
    xp = array_namespace(matrix)
    real_parts = quat_from_matrix_orthogonal(matrix[..., :3, :3])

    pure_translation_quats = xp.empty(
        (*matrix.shape[:-2], 4), dtype=matrix.dtype, device=xp_device(matrix)
    )
    pure_translation_quats = xpx.at(pure_translation_quats)[..., :3].set(
        matrix[..., :3, 3]
    )
    pure_translation_quats = xpx.at(pure_translation_quats)[..., 3].set(0.0)

    dual_parts = 0.5 * compose_quat(pure_translation_quats, real_parts)

    if scalar_first:
        real_parts = xp.roll(real_parts, 1, axis=-1)
        dual_parts = xp.roll(dual_parts, 1, axis=-1)

    dual_quats = xp.concat([real_parts, dual_parts], axis=-1)
    return dual_quats

