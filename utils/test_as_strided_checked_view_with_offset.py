
def test_as_strided_checked_view_with_offset():
    """Test as_strided

    - with check_bounds=True
    - on a view that doesn't start at the beginning.
    """
    a = np.arange(1000, dtype=np.int64)

    b = a[100:102]

    y = as_strided(b, shape=(2,), strides=(80,), check_bounds=True)
    assert_equal(y.shape, (2,))
    assert_equal(y[0], 100)
    assert_equal(y[1], 110)

