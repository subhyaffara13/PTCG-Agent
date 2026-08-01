
def test_histogram01(xp):
    expected = xp.ones(10)
    input = xp.arange(10)
    output = ndimage.histogram(input, 0, 10, 10)
    assert_array_almost_equal(output, expected)

