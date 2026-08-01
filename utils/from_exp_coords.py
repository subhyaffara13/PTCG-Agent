
def from_exp_coords(exp_coords: Array) -> Array:
    rot_vec = exp_coords[..., :3]
    rot_matrix = quat_as_matrix(quat_from_rotvec(rot_vec))
    translation_transform = _compute_se3_exp_translation_transform(rot_vec)
    translations = (translation_transform @ exp_coords[..., 3:, None])[..., 0]
    return _create_transformation_matrix(translations, rot_matrix)

