
def test_identity_shape():  # Not an xp test, identity is using numpy only for now
    r = Rotation.identity(shape=())
    assert r.as_quat().shape == (4,)
    r = Rotation.identity(shape=5)  # Shape can be int
    assert r.as_quat().shape == (5, 4)
    r = Rotation.identity(shape=(2, 3))
    assert r.as_quat().shape == (2, 3, 4)
    # Test values
    r = Rotation.identity(shape=(2, 2, 3))
    xp_assert_equal(r.as_quat().reshape(-1, 4), np.tile(np.eye(4)[-1], (2 * 2 * 3, 1)))
    # Errors
    with pytest.raises(ValueError, match="`shape` must be an int or a tuple of ints"):
        Rotation.identity(shape=2.5)
    with pytest.raises(ValueError, match="Only one of `num` or `shape` can be"):
        Rotation.identity(num=3, shape=(2, 2))
    with pytest.raises(TypeError, match="takes from 0 to 1 positional arguments"):
        Rotation.identity(3, 3)

