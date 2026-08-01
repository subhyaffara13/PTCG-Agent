
def test_SimplePatchShadow_offset():
    pe = path_effects.SimplePatchShadow(offset=(4, 5))
    assert pe._offset == (4, 5)

