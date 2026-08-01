
def test_maximum_position06(xp):
    labels = xp.asarray([1, 2, 0, 4])
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[5, 4, 2, 5],
                            [3, 7, 8, 2],
                            [1, 5, 1, 1]], dtype=dtype)
        output = ndimage.maximum_position(input, labels,
                                          xp.asarray([1, 2]))
        assert output[0] == (0, 0)
        assert output[1] == (1, 1)

