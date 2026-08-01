
def test_standard_deviation04(xp):
    input = np.asarray([1, 0], dtype=bool)
    input = xp.asarray(input)
    output = ndimage.standard_deviation(input)
    assert_almost_equal(output, xp.asarray(0.5), check_0d=False)

