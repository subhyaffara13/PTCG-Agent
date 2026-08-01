
def test_multiple_modes_laplace(xp):
    # Test laplace filter for multiple extrapolation modes
    arr = xp.asarray([[1., 0., 0.],
                      [1., 1., 0.],
                      [0., 0., 0.]])

    expected = xp.asarray([[-2., 2., 1.],
                           [-2., -3., 2.],
                           [1., 1., 0.]])

    modes = ['reflect', 'wrap']

    xp_assert_equal(expected,
                 ndimage.laplace(arr, mode=modes))

