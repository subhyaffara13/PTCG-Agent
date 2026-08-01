
def test_from_single_nd_matrix(xp, ndim: int):
    mat = xp.asarray([
            [0, 0, 1],
            [1, 0, 0],
            [0, 1, 0]
            ])
    mat = xp.reshape(mat, (1,) * (ndim - 1) + (3, 3))
    expected_quat = xp.asarray([0.5, 0.5, 0.5, 0.5])
    expected_quat = xp.reshape(expected_quat, (1,) * (ndim - 1) + (4,))
    xp_assert_close(Rotation.from_matrix(mat).as_quat(), expected_quat)

