
def test_variance02(xp):
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([1], dtype=dtype)
        output = ndimage.variance(input)
        assert_almost_equal(output, xp.asarray(0.0), check_0d=False)

