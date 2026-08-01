
def test_rotation_within_numpy_array():
    # TODO: Do we want to support this for all Array API frameworks?
    single = Rotation.random(rng=0)
    multiple = Rotation.random(2, rng=1)

    array = np.array(single)
    assert_equal(array.shape, ())

    array = np.array(multiple)
    assert_equal(array.shape, (2,))
    xp_assert_close(array[0].as_matrix(), multiple[0].as_matrix())
    xp_assert_close(array[1].as_matrix(), multiple[1].as_matrix())

    array = np.array([single])
    assert_equal(array.shape, (1,))
    assert_equal(array[0], single)

    array = np.array([multiple])
    assert_equal(array.shape, (1, 2))
    xp_assert_close(array[0, 0].as_matrix(), multiple[0].as_matrix())
    xp_assert_close(array[0, 1].as_matrix(), multiple[1].as_matrix())

    array = np.array([single, multiple], dtype=object)
    assert_equal(array.shape, (2,))
    assert_equal(array[0], single)
    assert_equal(array[1], multiple)

    array = np.array([multiple, multiple, multiple])
    assert_equal(array.shape, (3, 2))

