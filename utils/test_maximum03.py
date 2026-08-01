
def test_maximum03(xp):
    labels = xp.asarray([1, 2])
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[1, 2], [3, 4]], dtype=dtype)
        output = ndimage.maximum(input, labels=labels,
                                 index=2)
        assert_almost_equal(output, xp.asarray(4.0), check_0d=False)

