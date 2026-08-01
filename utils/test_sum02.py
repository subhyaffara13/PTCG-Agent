
def test_sum02(xp):
    for type in types:
        dtype = getattr(xp, type)
        input = xp.zeros([0, 4], dtype=dtype)
        output = ndimage.sum(input)
        assert output == 0

