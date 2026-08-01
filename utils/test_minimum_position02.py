
def test_minimum_position02(xp):
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[5, 4, 2, 5],
                            [3, 7, 0, 2],
                            [1, 5, 1, 1]], dtype=dtype)
        output = ndimage.minimum_position(input)
        assert output == (1, 2)

