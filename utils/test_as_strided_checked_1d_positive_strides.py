
def test_as_strided_checked_1d_positive_strides(size, view_size, stride_mult):
    """Test 1D arrays with positive strides."""
    x = np.arange(size, dtype=np.int64)
    itemsize = x.itemsize
    y = as_strided(
        x, shape=(view_size,), strides=(itemsize * stride_mult,), check_bounds=True
    )
    assert y.shape == (view_size,)
    # Verify data correctness
    expected = x[::stride_mult][:view_size]
    assert_array_equal(y, expected)

