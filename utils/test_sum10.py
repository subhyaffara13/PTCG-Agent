
def test_sum10(xp):
    labels = np.asarray([1, 0], dtype=bool)
    input = np.asarray([[1, 2], [3, 4]], dtype=bool)

    labels = xp.asarray(labels)
    input = xp.asarray(input)
    output = ndimage.sum(input, labels=labels)
    assert_almost_equal(output, xp.asarray(2.0), check_0d=False)

