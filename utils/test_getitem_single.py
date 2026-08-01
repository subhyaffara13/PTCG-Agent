
def test_getitem_single(xp):
    with pytest.raises(TypeError, match='not subscriptable'):
        Rotation.from_quat(xp.asarray([0, 0, 0, 1]))[0]

