
def test_from_matrix_normalize(xp):
    mat = xp.asarray([
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 1]])
    expected = xp.asarray([[ 0.894427, 0.447214, 0.0],
                           [-0.447214, 0.894427, 0.0],
                           [ 0.0,      0.0,      1.0]])
    xp_assert_close(Rotation.from_matrix(mat).as_matrix(), expected, atol=1e-6)

    mat = xp.asarray([
        [0,  -0.5, 0  ],
        [0.5, 0  , 0  ],
        [0,   0  , 0.5]])
    expected = xp.asarray([[0.0, -1, 0],
                           [  1,  0, 0],
                           [  0,  0, 1]])
    xp_assert_close(Rotation.from_matrix(mat).as_matrix(), expected, atol=1e-6)

    # Test a mix of normalized and non-normalized matrices
    mat = xp.stack([mat, xp.eye(3)])
    expected = xp.stack([expected, xp.eye(3)])
    xp_assert_close(Rotation.from_matrix(mat).as_matrix(), expected, atol=1e-6)

