
def test_sum05(xp):
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[1, 2], [3, 4]], dtype=dtype)
        output = ndimage.sum(input)
        assert_almost_equal(output, xp.asarray(10.0), check_0d=False)

