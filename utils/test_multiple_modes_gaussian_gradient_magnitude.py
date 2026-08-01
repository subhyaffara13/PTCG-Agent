
def test_multiple_modes_gaussian_gradient_magnitude(xp):
    # Test gaussian_gradient_magnitude filter for multiple
    # extrapolation modes
    arr = xp.asarray([[1., 0., 0.],
                      [1., 1., 0.],
                      [0., 0., 0.]])

    expected = xp.asarray([[0.04928965, 0.09745625, 0.06405368],
                           [0.23056905, 0.14025305, 0.04550846],
                           [0.19894369, 0.14950060, 0.06796850]])

    modes = ['reflect', 'wrap']

    calculated = ndimage.gaussian_gradient_magnitude(arr, 1, mode=modes)

    assert_almost_equal(expected, calculated)

