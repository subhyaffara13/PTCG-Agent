
def test__validate_vector():
    x = [1, 2, 3]
    y = _validate_vector(x)
    assert_array_equal(y, x)

    y = _validate_vector(x, dtype=np.float64)
    assert_array_equal(y, x)
    assert_equal(y.dtype, np.float64)

    x = [1]
    y = _validate_vector(x)
    assert_equal(y.ndim, 1)
    assert_equal(y, x)

    x = 1
    with pytest.raises(ValueError, match="Input vector should be 1-D"):
        _validate_vector(x)

    x = np.arange(5).reshape(1, -1, 1)
    with pytest.raises(ValueError, match="Input vector should be 1-D"):
        _validate_vector(x)

    x = [[1, 2], [3, 4]]
    with pytest.raises(ValueError, match="Input vector should be 1-D"):
        _validate_vector(x)

