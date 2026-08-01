
def test_label06(xp):
    data = xp.asarray([1, 0, 1, 1, 0, 1])
    out, n = ndimage.label(data)
    assert_array_almost_equal(out, xp.asarray([1, 0, 2, 2, 0, 3]))
    assert n == 3

