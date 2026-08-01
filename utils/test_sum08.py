
def test_sum08(xp):
    labels = np.asarray([1, 0], dtype=bool)
    labels = xp.asarray(labels)
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([1, 2], dtype=dtype)
        output = ndimage.sum(input, labels=labels)
        assert output == 1

