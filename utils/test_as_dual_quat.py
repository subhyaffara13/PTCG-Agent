
def test_as_dual_quat(xp, ndim: int):
    dtype = xpx.default_dtype(xp)
    shape = (ndim,) * (ndim - 1)
    # identity
    expected = xp.asarray([0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0], dtype=dtype)
    actual = rigid_transform_to_xp(RigidTransform.identity(), xp).as_dual_quat()
    xp_assert_close(actual, expected, atol=1e-12)

    expected = xp.asarray([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    tf = rigid_transform_to_xp(RigidTransform.identity(), xp)
    actual = tf.as_dual_quat(scalar_first=True)
    xp_assert_close(actual, expected, atol=1e-12)

    rng = np.random.default_rng(10)

    # only rotation
    for _ in range(10):
        q = xp.asarray(rng.normal(size=shape + (4,)), dtype=dtype)
        real_part = Rotation.from_quat(q).as_quat()
        dual_part = xp.zeros_like(real_part)
        expected = xp.concat((real_part, dual_part), axis=-1)
        actual = RigidTransform.from_dual_quat(expected).as_dual_quat()
        # because of double cover:
        actual = actual * xp.sign(actual[..., 0, None])
        expected = expected * xp.sign(expected[..., 0, None])
        xp_assert_close(actual, expected, atol=1e-12)

    # only translation
    for _ in range(10):
        tf = 0.5 * xp.asarray(rng.normal(size=shape + (3,)), dtype=dtype)
        expected = xp.zeros(shape + (8,), dtype=dtype)
        expected = xpx.at(expected)[..., 3].set(1.0)
        expected = xpx.at(expected)[..., 4:7].set(tf)
        actual = RigidTransform.from_dual_quat(expected).as_dual_quat()
        # because of double cover:
        actual = actual * xp.sign(actual[..., 0, None])
        expected = expected * xp.sign(expected[..., 0, None])
        xp_assert_close(actual, expected, atol=1e-12)

    # rotation and translation
    for _ in range(10):
        t = xp.asarray(rng.normal(size=shape + (3,)), dtype=dtype)
        r = Rotation.from_quat(xp.asarray(rng.normal(size=shape + (4,)), dtype=dtype))
        expected = RigidTransform.from_components(t, r).as_dual_quat()
        actual = RigidTransform.from_dual_quat(expected).as_dual_quat()
        # because of double cover:
        actual = actual * xp.sign(actual[..., 0, None])
        expected = expected * xp.sign(expected[..., 0, None])
        xp_assert_close(actual, expected, atol=1e-12)

