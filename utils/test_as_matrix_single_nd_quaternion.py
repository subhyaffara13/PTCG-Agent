
def test_as_matrix_single_nd_quaternion(xp, ndim: int):
    quat = xp.asarray([0, 0, 1, 1])
    quat = xp.reshape(quat, (1,) * (ndim - 1) + (4,))
    mat = Rotation.from_quat(quat).as_matrix()
    expected_mat = xp.asarray([
        [0.0, -1, 0],
        [1, 0, 0],
        [0, 0, 1]
        ])
    expected_mat = xp.reshape(expected_mat, (1,) * (ndim - 1) + (3, 3))
    xp_assert_close(mat, expected_mat, atol=1e-16)

