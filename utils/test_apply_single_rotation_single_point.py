
def test_apply_single_rotation_single_point(xp):
    dtype = xpx.default_dtype(xp)
    mat = xp.asarray([
        [0, -1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ])
    r_1d = Rotation.from_matrix(mat)
    r_2d = Rotation.from_matrix(xp.expand_dims(mat, axis=0))

    v_1d = xp.asarray([1.0, 2, 3], dtype=dtype)
    v_2d = xp.expand_dims(v_1d, axis=0)
    v1d_rotated = xp.asarray([-2.0, 1, 3], dtype=dtype)
    v2d_rotated = xp.expand_dims(v1d_rotated, axis=0)

    xp_assert_close(r_1d.apply(v_1d), v1d_rotated)
    xp_assert_close(r_1d.apply(v_2d), v2d_rotated)
    xp_assert_close(r_2d.apply(v_1d), v2d_rotated)
    xp_assert_close(r_2d.apply(v_2d), v2d_rotated)

    v1d_inverse = xp.asarray([2.0, -1, 3], dtype=dtype)
    v2d_inverse = xp.expand_dims(v1d_inverse, axis=0)

    xp_assert_close(r_1d.apply(v_1d, inverse=True), v1d_inverse)
    xp_assert_close(r_1d.apply(v_2d, inverse=True), v2d_inverse)
    xp_assert_close(r_2d.apply(v_1d, inverse=True), v2d_inverse)
    xp_assert_close(r_2d.apply(v_2d, inverse=True), v2d_inverse)

