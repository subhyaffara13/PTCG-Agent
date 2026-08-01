
def test_extrema02(xp):
    labels = xp.asarray([1, 2])
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[1, 2], [3, 4]], dtype=dtype)
        output1 = ndimage.extrema(input, labels=labels,
                                  index=2)
        output2 = ndimage.minimum(input, labels=labels,
                                  index=2)
        output3 = ndimage.maximum(input, labels=labels,
                                  index=2)
        output4 = ndimage.minimum_position(input,
                                           labels=labels, index=2)
        output5 = ndimage.maximum_position(input,
                                           labels=labels, index=2)
        assert output1 == (output2, output3, output4, output5)

