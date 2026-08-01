
def test_maximum05(xp):
    # Regression test for ticket #501 (Trac)
    x = xp.asarray([-3, -2, -1])
    assert ndimage.maximum(x) == -1

