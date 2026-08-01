
def test_label04(xp):
    data = xp.zeros([1])
    out, n = ndimage.label(data)
    assert_array_almost_equal(out, xp.asarray([0]))
    assert n == 0

