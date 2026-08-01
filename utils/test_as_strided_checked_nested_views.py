
def test_as_strided_checked_nested_views():
    """Test as_strided with check_bounds=True on a view of a view."""
    a = np.arange(1000, dtype=np.int64)
    b = a[10:100]
    c = b[5:10]

    y = as_strided(c, shape=(2,), strides=(160,), check_bounds=True)
    assert_equal(y.shape, (2,))
    assert_equal(y[0], 15)
    assert_equal(y[1], 35)

