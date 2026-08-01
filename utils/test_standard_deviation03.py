
def test_standard_deviation03(xp):
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([1, 3], dtype=dtype)
        output = ndimage.standard_deviation(input)
        assert_almost_equal(output, xp.asarray(1.0), check_0d=False)

