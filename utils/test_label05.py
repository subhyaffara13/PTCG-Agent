
def test_label05(xp):
    data = xp.ones([5])
    out, n = ndimage.label(data)
    assert_array_almost_equal(out, xp.asarray([1, 1, 1, 1, 1]))
    assert n == 1

