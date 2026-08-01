
def test_multiple_modes_uniform(xp):
    # Test uniform filter for multiple extrapolation modes
    arr = xp.asarray([[1., 0., 0.],
                      [1., 1., 0.],
                      [0., 0., 0.]])

    expected = xp.asarray([[0.32, 0.40, 0.48],
                           [0.20, 0.28, 0.32],
                           [0.28, 0.32, 0.40]])

    modes = ['reflect', 'wrap']

    assert_almost_equal(expected,
                        ndimage.uniform_filter(arr, 5, mode=modes))

