
def test_magnitude_single_rotation(xp):
    r = Rotation.from_quat(xp.eye(4))
    result1 = r[0].magnitude()
    xp_assert_close(result1, xp.asarray(xp.pi)[()])

    result2 = r[3].magnitude()
    xp_assert_close(result2, xp.asarray(0.0)[()])

