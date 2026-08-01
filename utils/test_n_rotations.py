
def test_n_rotations(xp):
    mat = np.empty((2, 3, 3))
    mat[0] = np.array([
        [0, -1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ])
    mat[1] = np.array([
        [1, 0, 0],
        [0, 0, -1],
        [0, 1, 0]
    ])
    mat = xp.asarray(mat)
    r = Rotation.from_matrix(mat)

    assert_equal(len(r), 2)
    assert_equal(len(r[:-1]), 1)

