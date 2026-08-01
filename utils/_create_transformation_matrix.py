
def _create_transformation_matrix(
    translations: Array, rotation_matrices: Array
) -> Array:
    if not translations.shape[:-1] == rotation_matrices.shape[:-2]:
        raise ValueError(
            "The number of rotation matrices and translations must be the same."
        )
    xp = array_namespace(translations)
    matrix = xp.empty(
        (*translations.shape[:-1], 4, 4),
        dtype=translations.dtype,
        device=xp_device(translations),
    )
    matrix = xpx.at(matrix)[..., :3, :3].set(rotation_matrices)
    matrix = xpx.at(matrix)[..., :3, 3].set(translations)
    matrix = xpx.at(matrix)[..., 3, :3].set(0)
    matrix = xpx.at(matrix)[..., 3, 3].set(1)
    return matrix

