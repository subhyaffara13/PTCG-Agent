
def test_multiple_modes_gaussian_laplace(xp):
    # Test gaussian_laplace filter for multiple extrapolation modes
    arr = xp.asarray([[1., 0., 0.],
                      [1., 1., 0.],
                      [0., 0., 0.]])

    expected = xp.asarray([[-0.28438687, 0.01559809, 0.19773499],
                           [-0.36630503, -0.20069774, 0.07483620],
                           [0.15849176, 0.18495566, 0.21934094]])

    modes = ['reflect', 'wrap']

    assert_almost_equal(expected,
                        ndimage.gaussian_laplace(arr, 1, mode=modes))

