
def test_zero_rotation_concatentation(xp):
    r = Rotation.from_quat(xp.zeros((0, 4)))

    r0 = Rotation.concatenate([r, r])
    assert len(r0) == 0

    r1 = Rotation.from_quat(xp.asarray([0.0, 0, 0, 1]))
    r1 = r.concatenate([r1, r])
    assert len(r1) == 1

    r3 = rotation_to_xp(Rotation.random(3), xp)
    r3 = r.concatenate([r3, r])
    assert len(r3) == 3

    r4 = rotation_to_xp(Rotation.random(4), xp)
    r4 = r.concatenate([r, r4])
    r4 = r.concatenate([r, r4])
    assert len(r4) == 4

