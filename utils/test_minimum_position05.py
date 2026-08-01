
def test_minimum_position05(xp):
    labels = xp.asarray([1, 2, 0, 4])
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[5, 4, 2, 5],
                            [3, 7, 0, 2],
                            [1, 5, 2, 3]], dtype=dtype)
        output = ndimage.minimum_position(input, labels)
        assert output == (2, 0)

