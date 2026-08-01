
def test_extrema01(xp):
    labels = np.asarray([1, 0], dtype=bool)
    labels = xp.asarray(labels)
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[1, 2], [3, 4]], dtype=dtype)
        output1 = ndimage.extrema(input, labels=labels)
        output2 = ndimage.minimum(input, labels=labels)
        output3 = ndimage.maximum(input, labels=labels)
        output4 = ndimage.minimum_position(input,
                                           labels=labels)
        output5 = ndimage.maximum_position(input,
                                           labels=labels)
        assert output1 == (output2, output3, output4, output5)

