
def test_minimum04(xp):
    labels = xp.asarray([[1, 2], [2, 3]])
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[1, 2], [3, 4]], dtype=dtype)
        output = ndimage.minimum(input, labels=labels,
                                 index=xp.asarray([2, 3, 8]))
        assert_array_almost_equal(output, xp.asarray([2.0, 4.0, 0.0]))

