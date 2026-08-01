
def test_setitem_single(xp):
    r = Rotation.from_quat(xp.asarray([0, 0, 0, 1]))
    with pytest.raises(TypeError, match='not subscriptable'):
        r[0] = Rotation.from_quat(xp.asarray([0, 0, 0, 1]))

