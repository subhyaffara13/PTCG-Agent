
def test_minimum_position06(xp):
    labels = xp.asarray([1, 2, 3, 4])
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[5, 4, 2, 5],
                            [3, 7, 0, 2],
                            [1, 5, 1, 1]], dtype=dtype)
        output = ndimage.minimum_position(input, labels, 2)
        assert output == (0, 1)

