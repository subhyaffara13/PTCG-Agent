
def test_sum07(xp):
    labels = np.ones([0, 4], dtype=bool)
    labels = xp.asarray(labels)
    for type in types:
        dtype = getattr(xp, type)
        input = xp.zeros([0, 4], dtype=dtype)
        output = ndimage.sum(input, labels=labels)
        assert output == 0

