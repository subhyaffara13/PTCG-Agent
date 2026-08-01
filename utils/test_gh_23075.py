
def test_gh_23075(samples, mode, size, expected):
    # results verified against SciPy 1.14.1, before the median_filter
    # overhaul
    sample_array = np.asarray(samples, dtype=np.float32)
    expected = np.asarray(expected, dtype=np.float32)
    filtered_samples = ndimage.median_filter(sample_array, size=size, mode=mode)
    xp_assert_close(filtered_samples, expected, check_shape=True, check_dtype=True)

