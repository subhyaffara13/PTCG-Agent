
def test_from_matrix_array_like():
    # Test single transform matrix
    matrix = [[1, 0, 0, 0],
              [0, 1, 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1]]
    expected = np.eye(4)
    tf = RigidTransform.from_matrix(matrix)
    xp_assert_close(tf.as_matrix(), expected)
    assert tf.single

    # Test multiple transform matrices
    matrices = [matrix, matrix]
    tf = RigidTransform.from_matrix(matrices)
    for i in range(len(matrices)):
        xp_assert_close(tf.as_matrix()[i, ...], expected)
    assert not tf.single


def test_from_matrix_array_like():
    rng = np.random.default_rng(123)
    # Single rotation
    r_expected = Rotation.random(rng=rng)
    r = Rotation.from_matrix(r_expected.as_matrix().tolist())
    assert r_expected.approx_equal(r, atol=1e-12)

    # Multiple rotations
    r_expected = Rotation.random(3, rng=rng)
    r = Rotation.from_matrix(r_expected.as_matrix().tolist())
    assert np.all(r_expected.approx_equal(r, atol=1e-12))

