import math


def test_from_euler_single_rotation(xp):
    quat = Rotation.from_euler("z", xp.asarray(90), degrees=True).as_quat()
    expected_quat = xp.asarray([0.0, 0, 1, 1]) / math.sqrt(2)
    xp_assert_close(quat, expected_quat)

