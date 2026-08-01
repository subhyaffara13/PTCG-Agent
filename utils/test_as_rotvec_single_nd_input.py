
def test_as_rotvec_single_nd_input(xp, ndim: int):
    quat = xp.asarray([1, 2, -3, 2])
    quat = xp.reshape(quat, (1,) * (ndim - 1) + (4,))
    expected_rotvec = xp.asarray([0.5772381, 1.1544763, -1.7317144])
    expected_rotvec = xp.reshape(expected_rotvec, (1,) * (ndim - 1) + (3,))
    actual_rotvec = Rotation.from_quat(quat).as_rotvec()

    assert_equal(actual_rotvec.shape, expected_rotvec.shape)
    xp_assert_close(actual_rotvec, expected_rotvec)

