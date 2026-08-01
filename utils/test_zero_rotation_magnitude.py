
def test_zero_rotation_magnitude(xp):
    r = Rotation.from_quat(xp.zeros((0, 4)))
    magnitude = r.magnitude()
    assert magnitude.shape == (0,)

