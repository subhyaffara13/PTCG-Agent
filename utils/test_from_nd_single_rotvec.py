
def test_from_nd_single_rotvec(xp, ndim: int):
    atol = 1e-7
    rotvec = xp.asarray([1, 0, 0])
    rotvec = xp.reshape(rotvec, (1,) * (ndim - 1) + (3,))
    expected_quat = xp.asarray([0.4794255, 0, 0, 0.8775826])
    expected_quat = xp.reshape(expected_quat, (1,) * (ndim - 1) + (4,))
    result = Rotation.from_rotvec(rotvec)
    xp_assert_close(result.as_quat(), expected_quat, atol=atol)

