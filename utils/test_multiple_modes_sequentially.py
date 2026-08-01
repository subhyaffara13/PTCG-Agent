
def test_multiple_modes_sequentially(xp):
    # Test that the filters with multiple mode capabilities for different
    # dimensions give the same result as applying the filters with
    # different modes sequentially
    arr = xp.asarray([[1., 0., 0.],
                      [1., 1., 0.],
                      [0., 0., 0.]])

    modes = ['reflect', 'wrap']

    expected = ndimage.gaussian_filter1d(arr, 1, axis=0, mode=modes[0])
    expected = ndimage.gaussian_filter1d(expected, 1, axis=1, mode=modes[1])
    xp_assert_equal(expected,
                 ndimage.gaussian_filter(arr, 1, mode=modes))

    expected = ndimage.uniform_filter1d(arr, 5, axis=0, mode=modes[0])
    expected = ndimage.uniform_filter1d(expected, 5, axis=1, mode=modes[1])
    xp_assert_equal(expected,
                 ndimage.uniform_filter(arr, 5, mode=modes))

    expected = ndimage.maximum_filter1d(arr, size=5, axis=0, mode=modes[0])
    expected = ndimage.maximum_filter1d(expected, size=5, axis=1,
                                        mode=modes[1])
    xp_assert_equal(expected,
                 ndimage.maximum_filter(arr, size=5, mode=modes))

    expected = ndimage.minimum_filter1d(arr, size=5, axis=0, mode=modes[0])
    expected = ndimage.minimum_filter1d(expected, size=5, axis=1,
                                        mode=modes[1])
    xp_assert_equal(expected,
                 ndimage.minimum_filter(arr, size=5, mode=modes))

