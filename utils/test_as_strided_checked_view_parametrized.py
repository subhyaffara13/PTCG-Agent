
def test_as_strided_checked_view_parametrized(start, stop, stride_bytes, should_pass):
    """Parametrized test for various view and stride combinations."""
    a = np.arange(100, dtype=np.int64)
    b = a[start:stop]

    if should_pass:
        y = as_strided(b, shape=(2,), strides=(stride_bytes,), check_bounds=True)
        assert_equal(y.shape, (2,))
    else:
        with pytest.raises(ValueError, match="out of bounds"):
            as_strided(b, shape=(2,), strides=(stride_bytes,), check_bounds=True)

