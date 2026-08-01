
def test_from_quat_scalar_first(xp):
    rng = np.random.RandomState(0)

    r = Rotation.from_quat(xp.asarray([1, 0, 0, 0]), scalar_first=True)
    xp_assert_close(r.as_matrix(), xp.eye(3), rtol=1e-15, atol=1e-16)

    q = xp.tile(xp.asarray([1, 0, 0, 0]), (10, 1))
    r = Rotation.from_quat(q, scalar_first=True)
    xp_assert_close(
        r.as_matrix(), xp.tile(xp.eye(3), (10, 1, 1)), rtol=1e-15, atol=1e-16
    )

    q = xp.asarray(rng.randn(100, 4))
    q /= xp_vector_norm(q, axis=1)[:, None]
    for i in range(q.shape[0]):  # Array API conforming loop
        qi = q[i, ...]
        r = Rotation.from_quat(qi, scalar_first=True)
        xp_assert_close(xp.roll(r.as_quat(), 1), qi, rtol=1e-15)

    r = Rotation.from_quat(q, scalar_first=True)
    xp_assert_close(xp.roll(r.as_quat(), 1, axis=1), q, rtol=1e-15)

