
def test_gaussian_filter_float16(xp):
    # gh-8207
    data = xp.asarray([1], dtype=xp.float16)
    sigma = 1.0
    with assert_raises(RuntimeError):
        ndimage.gaussian_filter(data, sigma)

