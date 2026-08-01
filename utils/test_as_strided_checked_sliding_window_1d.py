
def test_as_strided_checked_sliding_window_1d(shape, window_shape):
    """Test sliding window views in 1D."""
    x = np.arange(shape[0], dtype=np.int64)
    itemsize = x.itemsize
    n_windows = shape[0] - window_shape[0] + 1
    view_shape = (n_windows, window_shape[0])
    view_strides = (itemsize, itemsize)

    y = as_strided(x, shape=view_shape, strides=view_strides, check_bounds=True)
    assert y.shape == view_shape
    # Check first and last windows
    assert_array_equal(y[0], x[: window_shape[0]])
    assert_array_equal(y[-1], x[-window_shape[0] :])

