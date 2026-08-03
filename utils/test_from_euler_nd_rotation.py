import math


def test_from_euler_nd_rotation(xp, ndim: int):
    angles = xp.reshape(xp.asarray([0, 0, 90]), (1,) * (ndim - 1) + (3,))
    quat = Rotation.from_euler("xyz", angles, degrees=True).as_quat()
    expected_quat = xp.asarray([0.0, 0, 1, 1]) / math.sqrt(2)
    expected_quat = xp.reshape(expected_quat, (1,) * (ndim - 1) + (4,))
    xp_assert_close(quat, expected_quat)

