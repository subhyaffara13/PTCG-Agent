
def test_approx_equal_batched(xp):
    # Same shapes
    batch_shape = (2, 10, 3)
    rng = np.random.default_rng(0)
    p = Rotation.from_quat(rng.normal(size=batch_shape + (4,)))
    q = Rotation.from_quat(rng.normal(size=batch_shape + (4,)))
    r_mag = (p * q.inv()).magnitude()  # Must be computed as numpy array for np.median
    p = rotation_to_xp(p, xp)
    q = rotation_to_xp(q, xp)
    assert r_mag.shape == batch_shape
    # ensure we get mix of Trues and Falses
    atol = xp.asarray(np.median(r_mag))
    xp_assert_equal(p.approx_equal(q, atol), (xp.asarray(r_mag) < atol))

    # Broadcastable shapes of same length
    p = Rotation.from_quat(rng.normal(size=batch_shape + (4,)))
    q = Rotation.from_quat(rng.normal(size=(1, 10, 1, 4)))
    r_mag = (p * q.inv()).magnitude()
    p = rotation_to_xp(p, xp)
    q = rotation_to_xp(q, xp)
    assert r_mag.shape == batch_shape
    atol = xp.asarray(np.median(r_mag))
    xp_assert_equal(p.approx_equal(q, atol), (xp.asarray(r_mag) < atol))

    # Broadcastable shapes of different length
    p = Rotation.from_quat(rng.normal(size=batch_shape + (4,)))
    q = Rotation.from_quat(rng.normal(size=(1, 3, 4)))
    r_mag = (p * q.inv()).magnitude()
    p = rotation_to_xp(p, xp)
    q = rotation_to_xp(q, xp)
    assert r_mag.shape == batch_shape
    atol = xp.asarray(np.median(r_mag))
    xp_assert_equal(p.approx_equal(q, atol), (xp.asarray(r_mag) < atol))

