
def test_getitem_array_like():
    mat = np.array([[[0.0, -1, 0],
                     [1, 0, 0],
                     [0, 0, 1]],
                    [[1, 0, 0],
                     [0, 0, -1],
                     [0, 1, 0]]])
    r = Rotation.from_matrix(mat)
    xp_assert_close(r[[0]].as_matrix(), mat[[0]], atol=1e-15)
    xp_assert_close(r[[0, 1]].as_matrix(), mat[[0, 1]], atol=1e-15)

