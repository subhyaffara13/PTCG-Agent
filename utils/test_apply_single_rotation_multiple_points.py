
def test_apply_single_rotation_multiple_points(xp, ndim: int):
    dtype = xpx.default_dtype(xp)
    mat = xp.asarray([
        [0, -1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ])
    r1 = Rotation.from_matrix(mat)
    r2 = Rotation.from_matrix(xp.expand_dims(mat, axis=0))

    rng = np.random.default_rng(0)
    batch_shape = (ndim,) * (ndim - 1)
    v = xp.asarray(rng.normal(size=batch_shape + (2, 3)), dtype=dtype)
    v_rotated = xp.stack([-v[..., 1], v[..., 0], v[..., 2]], axis=-1)

    xp_assert_close(r1.apply(v), v_rotated)
    xp_assert_close(r2.apply(v), v_rotated)

    v_inverse = xp.stack([v[..., 1], -v[..., 0], v[..., 2]], axis=-1)

    xp_assert_close(r1.apply(v, inverse=True), v_inverse)
    xp_assert_close(r2.apply(v, inverse=True), v_inverse)

