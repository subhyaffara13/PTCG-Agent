
def test_single_identity_magnitude(xp):
    r = rotation_to_xp(Rotation.identity(), xp)
    assert r.magnitude() == 0
    assert r.inv().magnitude() == 0

