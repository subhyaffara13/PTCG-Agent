
def test_as_strided_checked_view_out_of_bounds_negative():
    """Test that negative strides on a view correctly detect out of bounds."""
    a = np.arange(1000, dtype=np.int64)

    b = a[5:7]

    with pytest.raises(ValueError, match="out of bounds"):
        as_strided(b, shape=(2,), strides=(-48,), check_bounds=True)

