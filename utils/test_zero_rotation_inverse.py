
def test_zero_rotation_inverse(xp):
    r = Rotation.from_quat(xp.zeros((0, 4)))
    r_inv = r.inv()
    assert len(r_inv) == 0

