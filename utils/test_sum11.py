
def test_sum11(xp):
    labels = xp.asarray([1, 2], dtype=xp.int8)
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[1, 2], [3, 4]], dtype=dtype)
        output = ndimage.sum(input, labels=labels,
                             index=2)
        assert_almost_equal(output, xp.asarray(6.0), check_0d=False)

