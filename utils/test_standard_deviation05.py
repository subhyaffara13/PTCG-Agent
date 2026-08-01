
def test_standard_deviation05(xp):
    labels = xp.asarray([2, 2, 3])
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([1, 3, 8], dtype=dtype)
        output = ndimage.standard_deviation(input, labels, 2)
        assert_almost_equal(output, xp.asarray(1.0), check_0d=False)

