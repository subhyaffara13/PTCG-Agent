
def test_histogram02(xp):
    labels = xp.asarray([1, 1, 1, 1, 2, 2, 2, 2])
    expected = xp.asarray([0, 2, 0, 1, 1])
    input = xp.asarray([1, 1, 3, 4, 3, 3, 3, 3])
    output = ndimage.histogram(input, 0, 4, 5, labels, 1)
    assert_array_almost_equal(output, expected)

