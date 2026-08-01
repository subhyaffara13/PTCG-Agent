
def test_sum01(xp):
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([], dtype=dtype)
        output = ndimage.sum(input)
        assert output == 0

