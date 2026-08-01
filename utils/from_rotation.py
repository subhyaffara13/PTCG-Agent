
def from_rotation(quat: Array) -> Array:
    xp = array_namespace(quat)
    rotmat = quat_as_matrix(quat)
    matrix = xp.zeros(
        (*rotmat.shape[:-2], 4, 4), dtype=quat.dtype, device=xp_device(quat)
    )
    matrix = xpx.at(matrix)[..., :3, :3].set(rotmat)
    matrix = xpx.at(matrix)[..., 3, 3].set(1)
    return matrix

