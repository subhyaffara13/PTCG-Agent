
def test_random_rotation():
    # No xp testing since random rotations are always using NumPy
    rng = np.random.default_rng(0)
    assert_equal(Rotation.random(rng=rng).as_quat().shape, (4,))
    assert_equal(Rotation.random(None, rng=rng).as_quat().shape, (4,))
    assert_equal(Rotation.random(1, rng=rng).as_quat().shape, (1, 4))
    assert_equal(Rotation.random(5, rng=rng).as_quat().shape, (5, 4))
    # Shape argument
    assert_equal(Rotation.random(rng=rng, shape=()).as_quat().shape, (4,))
    assert_equal(Rotation.random(rng=rng, shape=(3,)).as_quat().shape, (3, 4))
    assert_equal(Rotation.random(rng=rng, shape=(2, 3)).as_quat().shape, (2, 3, 4))
    # Values should be the same for num=prod(shape)
    rng1, rng2 = np.random.default_rng(42), np.random.default_rng(42)
    r_num = Rotation.random(6, rng=rng1)
    r_shape = Rotation.random(rng=rng2, shape=(2, 3))
    xp_assert_close(r_num.as_quat(), r_shape.as_quat().reshape(6, 4), atol=1e-12)
    # Errors
    with pytest.raises(ValueError, match="Only one of `num` or `shape` can be"):
        Rotation.random(num=3,rng=rng, shape=(2, 2))
    with pytest.raises(ValueError, match="`shape` must be an int or a tuple of ints"):
        Rotation.random(rng=rng, shape=2.5)
    with pytest.raises(TypeError, match="takes from 0 to 2 positional arguments"):
        Rotation.random(1, rng, None)  # Shape should be kwarg only

