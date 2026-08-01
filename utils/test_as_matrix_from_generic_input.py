
def test_as_matrix_from_generic_input(xp):
    quats = xp.asarray([
            [0, 0, 1, 1],
            [0, 1, 0, 1],
            [1, 2, 3, 4]
            ])
    mat = Rotation.from_quat(quats).as_matrix()
    assert_equal(mat.shape, (3, 3, 3))

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

    expected2 = xp.asarray([
        [0.4, -2, 2.2],
        [2.8, 1, 0.4],
        [-1, 2, 2]
        ]) / 3
    xp_assert_close(mat[2, ...], expected2)

