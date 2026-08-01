
def test_non_contiguous_array(mode):
    arr = np.arange(24).reshape(4, 6)[::2, ::2]
    result = np.pad(arr, (2, 3), mode)
    assert result.shape == (7, 8)
    assert_equal(result[2:-3, 2:-3], arr)

