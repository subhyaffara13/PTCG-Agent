
def test_as_euler_nd_rotation(xp, ndim: int):
    mat = xp.asarray([
        [0.0, -1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ])
    mat = xp.reshape(mat, (1,) * (ndim - 1) + (3, 3))
    angles = Rotation.from_matrix(mat).as_euler("xyz", degrees=True)
    expected_angles = xp.asarray([0, 0, 90.0])
    expected_angles = xp.reshape(expected_angles, (1,) * (ndim - 1) + (3,))
    xp_assert_close(angles, expected_angles, atol=1e-12)

