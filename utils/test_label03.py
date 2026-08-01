
def test_label03(xp):
    data = xp.ones([1])
    out, n = ndimage.label(data)
    assert_array_almost_equal(out, xp.asarray([1]))
    assert n == 1

