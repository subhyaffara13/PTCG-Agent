
def test_setitem_wrong_type(xp):
    r = rotation_to_xp(Rotation.random(10, rng=0), xp)
    with pytest.raises(TypeError, match='Rotation object'):
        r[0] = 1

