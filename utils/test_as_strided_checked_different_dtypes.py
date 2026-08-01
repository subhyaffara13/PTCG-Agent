
def test_as_strided_checked_different_dtypes(dtype):
    """Test as_strided with check_bounds=True with different dtypes."""
    x = np.arange(10, dtype=dtype)
    y = as_strided(x, shape=(5,), strides=(x.itemsize * 2,), check_bounds=True)
    assert y.shape == (5,)
    assert y.dtype == dtype

