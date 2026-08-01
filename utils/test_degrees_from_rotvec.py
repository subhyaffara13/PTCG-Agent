
def test_degrees_from_rotvec(xp):
    rotvec1 = xp.asarray([1 / 3 ** (1/3)] * 3)
    rot1 = Rotation.from_rotvec(rotvec1, degrees=True)
    quat1 = rot1.as_quat()

    # deg2rad is not implemented in Array API -> / 180 * xp.pi
    rotvec2 = xp.asarray(rotvec1 / 180 * xp.pi)
    rot2 = Rotation.from_rotvec(rotvec2)
    quat2 = rot2.as_quat()

    xp_assert_close(quat1, quat2)

