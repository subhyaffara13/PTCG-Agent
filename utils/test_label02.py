
def test_label02(xp):
    data = xp.zeros(())
    out, n = ndimage.label(data)
    assert out == 0
    assert n == 0

