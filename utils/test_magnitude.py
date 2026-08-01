
def test_magnitude(xp, ndim: int):
    quat_shape = (1,) * (ndim - 1) + (4,)
    quat = xp.reshape(xp.eye(4), quat_shape + (4,))
    r = Rotation.from_quat(quat)
    result = r.magnitude()
    expected_result = xp.asarray([xp.pi, xp.pi, xp.pi, 0])
    expected_result = xp.reshape(expected_result, quat_shape)
    xp_assert_close(result, expected_result)

    r = Rotation.from_quat(-quat)
    result = r.magnitude()
    xp_assert_close(result, expected_result)

