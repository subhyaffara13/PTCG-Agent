
def test_label01(xp):
    data = xp.ones(())
    out, n = ndimage.label(data)
    assert out == 1
    assert n == 1

