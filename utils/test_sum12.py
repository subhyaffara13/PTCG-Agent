
def test_sum12(xp):
    labels = xp.asarray([[1, 2], [2, 4]], dtype=xp.int8)
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[1, 2], [3, 4]], dtype=dtype)
        output = ndimage.sum(input, labels=labels, index=xp.asarray([4, 8, 2]))
        assert_array_almost_equal(output, xp.asarray([4.0, 0.0, 5.0]))

