
def test_multiple_modes_sobel(xp):
    # Test sobel filter for multiple extrapolation modes

    arr = xp.asarray([[1., 0., 0.],
                      [1., 1., 0.],
                      [0., 0., 0.]])

    expected = xp.asarray([[1., -4., 3.],
                           [2., -3., 1.],
                           [1., -1., 0.]])

    modes = ['reflect', 'wrap']

    xp_assert_equal(expected,
                 ndimage.sobel(arr, mode=modes))

