
def from_matrix(matrix: Array, normalize: bool = True, copy: bool = True) -> Array:
    xp = array_namespace(matrix)
    # Shape check should be done before calling this function
    if normalize or copy:
        matrix = xp.asarray(matrix, copy=True)

    last_row_ok = xp.all(
        matrix[..., 3, :] == xp.asarray([0, 0, 0, 1.0], device=xp_device(matrix)),
        axis=-1,
    )
    lazy = is_lazy_array(matrix)
    # We delay lazy branch checks until after normalization to avoid overwriting nans
    # with the rotation matrix
    if not lazy and xp.any(~last_row_ok):
        if last_row_ok.shape == ():
            idx = ()
        else:
            idx = tuple(int(i[0]) for i in xp.nonzero(~last_row_ok))
        vals = matrix[idx + (3, ...)]
        raise ValueError(
            f"Expected last row of transformation matrix {idx} to be "
            f"exactly [0, 0, 0, 1], got {vals}"
        )

    # The quat_from_matrix() method orthogonalizes the rotation
    # component of the transformation matrix. While this does have some
    # overhead in converting a rotation matrix to a quaternion and back, it
    # allows for skipping singular value decomposition for near-orthogonal
    # matrices, which is a computationally expensive operation.
    if normalize:
        rotmat = quat_as_matrix(quat_from_matrix(matrix[..., :3, :3]))
        matrix = xpx.at(matrix)[..., :3, :3].set(rotmat)
    # Lazy branch matrix invalidation
    if lazy:
        matrix = xp.where(last_row_ok[..., None, None], matrix, xp.nan)
    return matrix


def from_matrix(matrix: Array, assume_valid: bool = False) -> Array:
    xp = array_namespace(matrix)
    device = xp_device(matrix)

    if not assume_valid:
        mask = xp.linalg.det(matrix) <= 0
        lazy = is_lazy_array(mask)
        # Only non-lazy backends raise an error for non-positive determinants.
        if not lazy and xp.any(mask):
            ind = int(xp.nonzero(xpx.atleast_nd(mask, ndim=1, xp=xp))[0][0])
            raise ValueError(
                "Non-positive determinant (left-handed or null coordinate frame) in "
                f"rotation matrix {ind}: {matrix[ind, ...]}."
            )
        elif lazy:
            matrix = xp.where(mask[..., None, None], xp.nan, matrix)

        gramians = matrix @ xp.matrix_transpose(matrix)
        eye = xp.eye(3, dtype=matrix.dtype, device=device)
        is_orthogonal = xp.all(
            xpx.isclose(gramians, eye, atol=1e-12, xp=xp), axis=(-2, -1)
        )

        if lazy:
            # Lazy backends do not support non-concrete boolean indexing or any form of
            # computation without statically known shapes, so we always compute SVD and
            # use xp.where to select the result.
            U, _, Vt = xp.linalg.svd(matrix, full_matrices=False)
            matrix = xp.where(is_orthogonal[..., None, None], matrix, U @ Vt)
        elif not xp.all(is_orthogonal):
            # For eager frameworks, only compute SVD if needed.
            is_not_orthogonal = ~is_orthogonal
            U, _, Vt = xp.linalg.svd(matrix[is_not_orthogonal], full_matrices=False)
            matrix = xpx.at(matrix)[is_not_orthogonal].set(U @ Vt)

    return _from_matrix_orthogonal(matrix)

