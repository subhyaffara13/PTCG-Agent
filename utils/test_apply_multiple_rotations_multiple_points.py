
def test_apply_multiple_rotations_multiple_points(xp, ndim: int):
    dtype = xpx.default_dtype(xp)
    mat = np.empty((2, 3, 3))
    mat[0] = np.array([
        [0, -1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ])
    mat[1] = np.array([
        [1, 0, 0],
        [0, 0, -1],
        [0, 1, 0]
    ])
    mat = xp.asarray(mat, dtype=dtype)
    batch_shape = (ndim,) * (ndim - 1)
    mat = xp.tile(mat, batch_shape + (1, 1, 1))
    r = Rotation.from_matrix(mat)

    v = xp.asarray([[1, 2, 3], [4, 5, 6]], dtype=dtype)
    v_rotated = xp.asarray([[-2.0, 1, 3], [4, -6, 5]], dtype=dtype)
    v_rotated = xp.tile(v_rotated, batch_shape + (1, 1))
    xp_assert_close(r.apply(v), v_rotated)

    v_inverse = xp.asarray([[2.0, -1, 3], [4, 6, -5]], dtype=dtype)
    v_inverse = xp.tile(v_inverse, batch_shape + (1, 1))
    xp_assert_close(r.apply(v, inverse=True), v_inverse)

