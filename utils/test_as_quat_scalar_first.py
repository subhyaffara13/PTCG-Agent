
def test_as_quat_scalar_first(xp):
    rng = np.random.RandomState(0)

    r = Rotation.from_euler('xyz', xp.zeros(3))
    xp_assert_close(r.as_quat(scalar_first=True), xp.asarray([1.0, 0, 0, 0]),
                    rtol=1e-15, atol=1e-16)

    r = Rotation.from_euler('xyz', xp.zeros((10, 3)))
    xp_assert_close(r.as_quat(scalar_first=True),
                    xp.tile(xp.asarray([1.0, 0, 0, 0]), (10, 1)),
                    rtol=1e-15, atol=1e-16)

    q = xp.asarray(rng.randn(100, 4))
    q /= xp_vector_norm(q, axis=1)[:, None]
    for i in range(q.shape[0]):  # Array API conforming loop
        qi = q[i, ...]
        r = Rotation.from_quat(qi)
        xp_assert_close(r.as_quat(scalar_first=True), xp.roll(qi, 1),
                        rtol=1e-15)

        xp_assert_close(r.as_quat(canonical=True, scalar_first=True),
                        xp.roll(r.as_quat(canonical=True), 1),
                        rtol=1e-15)

    r = Rotation.from_quat(q)
    xp_assert_close(r.as_quat(scalar_first=True), xp.roll(q, 1, axis=1),
                    rtol=1e-15)

    xp_assert_close(r.as_quat(canonical=True, scalar_first=True),
                    xp.roll(r.as_quat(canonical=True), 1, axis=1), rtol=1e-15)

