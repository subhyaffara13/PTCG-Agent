
def test_drm():
    assert drm(19, 12) == 7
    assert drm(2718, 10) == 2
    assert drm(0, 15) == 0
    assert drm(234161, 10) == 6
    raises(ValueError, lambda: drm(24, -2))
    raises(ValueError, lambda: drm(11.6, 9))

