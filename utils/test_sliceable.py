
def test_sliceable():
    sliceable = m.Sliceable(100)
    assert sliceable[::] == (0, 100, 1)
    assert sliceable[10::] == (10, 100, 1)
    assert sliceable[:10:] == (0, 10, 1)
    assert sliceable[::10] == (0, 100, 10)
    assert sliceable[-10::] == (90, 100, 1)
    assert sliceable[:-10:] == (0, 90, 1)
    assert sliceable[::-10] == (99, -1, -10)
    assert sliceable[50:60:1] == (50, 60, 1)
    assert sliceable[50:60:-1] == (50, 60, -1)

