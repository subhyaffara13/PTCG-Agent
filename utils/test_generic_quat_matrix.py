
def test_generic_quat_matrix(xp):
    x = xp.asarray([[3.0, 4, 0, 0], [5, 12, 0, 0]])
    r = Rotation.from_quat(x)
    expected_quat = x / xp.asarray([[5.0], [13.0]])
    xp_assert_close(r.as_quat(), expected_quat)

