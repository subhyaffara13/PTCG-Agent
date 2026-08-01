
def test_maximum_position01(xp):
    labels = np.asarray([1, 0], dtype=bool)
    labels = xp.asarray(labels)
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[1, 2], [3, 4]], dtype=dtype)
        output = ndimage.maximum_position(input,
                                          labels=labels)
        assert output == (1, 0)

