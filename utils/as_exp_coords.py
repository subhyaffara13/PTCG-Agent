
def as_exp_coords(matrix: Array) -> Array:
    xp = array_namespace(matrix)
    rot_vec = quat_as_rotvec(quat_from_matrix_orthogonal(matrix[..., :3, :3]))
    translation_transform = _compute_se3_log_translation_transform(rot_vec)
    translations = (translation_transform @ matrix[..., :3, 3][..., None])[..., 0]
    exp_coords = xp.concat([rot_vec, translations], axis=-1)
    return exp_coords

