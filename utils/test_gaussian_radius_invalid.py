
def test_gaussian_radius_invalid(xp):
    # radius must be a nonnegative integer
    with assert_raises(ValueError):
        ndimage.gaussian_filter1d(xp.zeros(8), sigma=1, radius=-1)
    with assert_raises(ValueError):
        ndimage.gaussian_filter1d(xp.zeros(8), sigma=1, radius=1.1)

