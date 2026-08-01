
def test_maximum02(xp):
    labels = np.asarray([1, 0], dtype=bool)
    input = np.asarray([[2, 2], [2, 4]], dtype=bool)
    labels = xp.asarray(labels)
    input = xp.asarray(input)
    output = ndimage.maximum(input, labels=labels)
    assert_almost_equal(output, xp.asarray(1.0), check_0d=False)

