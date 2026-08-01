
def test_multiple_modes_prewitt(xp):
    # Test prewitt filter for multiple extrapolation modes

    arr = xp.asarray([[1., 0., 0.],
                      [1., 1., 0.],
                      [0., 0., 0.]])

    expected = xp.asarray([[1., -3., 2.],
                           [1., -2., 1.],
                           [1., -1., 0.]])

    modes = ['reflect', 'wrap']

    xp_assert_equal(expected,
                 ndimage.prewitt(arr, mode=modes))

