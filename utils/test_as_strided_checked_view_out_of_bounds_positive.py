
def test_as_strided_checked_view_out_of_bounds_positive():
    """Test that positive strides on a view correctly detect out of bounds."""
    a = np.arange(100, dtype=np.int64)

    b = a[95:97]

    with pytest.raises(ValueError, match="out of bounds"):
        as_strided(b, shape=(2,), strides=(200,), check_bounds=True)

