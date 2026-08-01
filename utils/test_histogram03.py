
def test_histogram03(xp):
    labels = xp.asarray([1, 0, 1, 1, 2, 2, 2, 2])
    expected1 = xp.asarray([0, 1, 0, 1, 1])
    expected2 = xp.asarray([0, 0, 0, 3, 0])
    input = xp.asarray([1, 1, 3, 4, 3, 5, 3, 3])

    output = ndimage.histogram(input, 0, 4, 5, labels, (1, 2))

    assert_array_almost_equal(output[0], expected1)
    assert_array_almost_equal(output[1], expected2)

