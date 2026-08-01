
def test_sum06(xp):
    labels = np.asarray([], dtype=bool)
    labels = xp.asarray(labels)
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([], dtype=dtype)
        output = ndimage.sum(input, labels=labels)
        assert output == 0

