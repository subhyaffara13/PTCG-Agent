
def test_sum09(xp):
    labels = np.asarray([1, 0], dtype=bool)
    labels = xp.asarray(labels)
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[1, 2], [3, 4]], dtype=dtype)
        output = ndimage.sum(input, labels=labels)
        assert_almost_equal(output, xp.asarray(4.0), check_0d=False)

