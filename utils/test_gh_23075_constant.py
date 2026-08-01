
def test_gh_23075_constant(samples, size, cval, expected):
    # results verified against SciPy 1.14.1, before the median_filter
    # overhaul
    sample_array = np.asarray(samples, dtype=np.single)
    expected = np.asarray(expected, dtype=np.single)
    filtered_samples = ndimage.median_filter(sample_array,
                                             size=size,
                                             mode="constant",
                                             cval=cval)
    xp_assert_close(filtered_samples, expected, check_shape=True, check_dtype=True)

