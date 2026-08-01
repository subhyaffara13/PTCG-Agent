
def test_orders_gauss(xp):
    # Check order inputs to Gaussians
    arr = xp.zeros((1,))
    xp_assert_equal(ndimage.gaussian_filter(arr, 1, order=0), xp.asarray([0.]))
    xp_assert_equal(ndimage.gaussian_filter(arr, 1, order=3), xp.asarray([0.]))
    assert_raises(ValueError, ndimage.gaussian_filter, arr, 1, -1)
    xp_assert_equal(ndimage.gaussian_filter1d(arr, 1, axis=-1, order=0),
                    xp.asarray([0.]))
    xp_assert_equal(ndimage.gaussian_filter1d(arr, 1, axis=-1, order=3),
                    xp.asarray([0.]))
    assert_raises(ValueError, ndimage.gaussian_filter1d, arr, 1, -1, -1)

