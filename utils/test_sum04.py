
def test_sum04(xp):
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([1, 2], dtype=dtype)
        output = ndimage.sum(input)
        assert_almost_equal(output, xp.asarray(3.0), check_0d=False)

