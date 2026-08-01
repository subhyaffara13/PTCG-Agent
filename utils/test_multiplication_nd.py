
def test_multiplication_nd(xp):
    # multiple dimensions
    rng = np.random.default_rng(0)
    r1 = Rotation.from_quat(xp.asarray(rng.normal(size=(2, 3, 4))))
    r2 = Rotation.from_quat(xp.asarray(rng.normal(size=(2, 3, 4))))
    r3 = r1 * r2
    assert r3.as_quat().shape == (2, 3, 4)

    # same shape len, different dimensions
    r1 = Rotation.from_quat(xp.asarray(rng.normal(size=(1, 3, 4))))
    r2 = Rotation.from_quat(xp.asarray(rng.normal(size=(2, 1, 4))))
    r3 = r1 * r2
    assert r3.as_quat().shape == (2, 3, 4)

    # different shape len, different dimensions
    r1 = Rotation.from_quat(xp.asarray(rng.normal(size=(3, 1, 4, 4))))
    r2 = Rotation.from_quat(xp.asarray(rng.normal(size=(2, 4, 4))))
    r3 = r1 * r2
    assert r3.as_quat().shape == (3, 2, 4, 4)

    # transition between 2D and 3D with 2D rotation as first argument. This needs to
    # choose the xp_backend even though r1's backend is cython
    r1 = Rotation.from_quat(xp.asarray(rng.normal(size=(2, 4))))
    r2 = Rotation.from_quat(xp.asarray(rng.normal(size=(2, 2, 4))))
    r3 = r1 * r2
    assert r3.as_quat().shape == (2, 2, 4)

