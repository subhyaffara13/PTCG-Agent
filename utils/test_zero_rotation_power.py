
def test_zero_rotation_power(xp):
    r = Rotation.from_quat(xp.zeros((0, 4)))
    for pp in [-1.5, -1, 0, 1, 1.5]:
        pow0 = r**pp
        assert len(pow0) == 0

