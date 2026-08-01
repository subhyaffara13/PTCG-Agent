
def test_median_filter_lim2():
    sample_array = np.ones(8)
    expected = np.ones(8)
    filtered_samples = ndimage.median_filter(sample_array, size=19, mode="reflect")
    xp_assert_close(filtered_samples, expected, check_shape=True, check_dtype=True)

