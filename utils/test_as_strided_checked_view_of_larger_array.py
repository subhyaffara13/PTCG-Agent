
def test_as_strided_checked_view_of_larger_array():
    """Test as_strided

    - with check_bounds=True
    - considers the base array bounds, not just the view.

    """
    a = np.arange(1000, dtype=np.int64)

    b = a[:2]

    # This should succeed because the underlying array has enough memory
    y = as_strided(b, shape=(2,), strides=(400,), check_bounds=True)
    assert_equal(y.shape, (2,))
    assert_equal(y[0], 0)
    assert_equal(y[1], 50)

