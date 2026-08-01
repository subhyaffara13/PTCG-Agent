
def test_sum03(xp):
    for type in types:
        dtype = getattr(xp, type)
        input = xp.ones([], dtype=dtype)
        output = ndimage.sum(input)
        assert_almost_equal(output, xp.asarray(1.0), check_0d=False)

