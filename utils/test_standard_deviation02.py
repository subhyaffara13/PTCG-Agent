
def test_standard_deviation02(xp):
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([1], dtype=dtype)
        output = ndimage.standard_deviation(input)
        assert_almost_equal(output, xp.asarray(0.0), check_0d=False)

