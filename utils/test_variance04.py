
def test_variance04(xp):
    input = np.asarray([1, 0], dtype=bool)
    input = xp.asarray(input)
    output = ndimage.variance(input)
    assert_almost_equal(output, xp.asarray(0.25), check_0d=False)

