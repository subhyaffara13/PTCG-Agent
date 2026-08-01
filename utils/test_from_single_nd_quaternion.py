
def test_from_single_nd_quaternion(xp, ndim: int):
    x = xp.asarray([3.0, 4, 0, 0])
    x = xp.reshape(x, (1,) * (ndim - 1) + (4,))
    r = Rotation.from_quat(x)
    expected_quat = x / 5
    xp_assert_close(r.as_quat(), expected_quat)

