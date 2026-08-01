
def test_as_matrix_from_square_input(xp):
    quats = xp.asarray([
            [0, 0, 1, 1],
            [0, 1, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, -1]
            ])
    mat = Rotation.from_quat(quats).as_matrix()
    assert_equal(mat.shape, (4, 3, 3))

    expected0 = xp.asarray([
        [0.0, -1, 0],
        [1, 0, 0],
        [0, 0, 1]
        ])
    xp_assert_close(mat[0, ...], expected0, atol=1e-16)

    expected1 = xp.asarray([
        [0.0, 0, 1],
        [0, 1, 0],
        [-1, 0, 0]
        ])
    xp_assert_close(mat[1, ...], expected1, atol=1e-16)
    xp_assert_close(mat[2, ...], xp.eye(3))
    xp_assert_close(mat[3, ...], xp.eye(3))

