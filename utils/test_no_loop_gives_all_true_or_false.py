
def test_no_loop_gives_all_true_or_false(dt1, dt2):
    # Make sure they broadcast to test result shape, use random values, since
    # the actual value should be ignored
    arr1 = np.random.randint(5, size=100).astype(dt1)
    arr2 = np.random.randint(5, size=99)[:, np.newaxis].astype(dt2)

    res = arr1 == arr2
    assert res.shape == (99, 100)
    assert res.dtype == bool
    assert not res.any()

    res = arr1 != arr2
    assert res.shape == (99, 100)
    assert res.dtype == bool
    assert res.all()

    # incompatible shapes raise though
    arr2 = np.random.randint(5, size=99).astype(dt2)
    with pytest.raises(ValueError):
        arr1 == arr2

    with pytest.raises(ValueError):
        arr1 != arr2

    # Basic test with another operation:
    with pytest.raises(np._core._exceptions._UFuncNoLoopError):
        arr1 > arr2

