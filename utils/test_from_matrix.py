
def test_from_matrix(xp, ndim: int):
    atol = 1e-12
    shape = (ndim,) * (ndim - 1) + (4, 4)
    dtype = xpx.default_dtype(xp)

    matrix = xp.tile(xp.eye(4), shape[:-2] + (1, 1))
    t = xp.reshape(xp.arange(ndim ** (ndim-1) * 3, dtype=dtype), shape[:-2] + (3,))
    matrix = xpx.at(matrix)[..., :3, 3].set(t)

    tf = RigidTransform.from_matrix(matrix)
    xp_assert_close(tf.as_matrix(), matrix, atol=atol)
    assert tf.single == (ndim == 1)

    # Test non-1 determinant
    matrix = xp.tile(xp.eye(4), shape[:-2] + (1, 1))
    matrix = xpx.at(matrix)[..., :3, :3].set(xp.eye(3) * 2.0)
    tf = RigidTransform.from_matrix(matrix)
    expected = xp.tile(xp.eye(4), shape[:-2] + (1, 1))
    xp_assert_close(tf.as_matrix(), expected, atol=atol)

    # Test non-orthogonal rotation matrix
    matrix = xp.tile(xp.eye(4), shape[:-2] + (1, 1))
    # matrix is equivalent to [[1, 1, 0, 0],
    #                          [0, 1, 0, 0],
    #                          [0, 0, 1, 0],
    #                          [0, 0, 0, 1]]
    matrix = xpx.at(matrix)[..., 0, 1].set(1.0)
    tf = RigidTransform.from_matrix(matrix)
    expected = xp.tile(xp.eye(4), shape[:-2] + (1, 1))
    expected = xpx.at(expected)[..., 0, 0].set(0.894427)
    expected = xpx.at(expected)[..., 0, 1].set(0.447214)
    expected = xpx.at(expected)[..., 1, 0].set(-0.447214)
    expected = xpx.at(expected)[..., 1, 1].set(0.894427)
    xp_assert_close(tf.as_matrix(), expected, atol=1e-6)

    # Test invalid matrix
    invalid = xp.tile(xp.eye(4), shape[:-2] + (1, 1))
    invalid = xpx.at(invalid)[..., 3, 3].set(2)  # Invalid last row
    if is_lazy_array(invalid):
        tf = RigidTransform.from_matrix(invalid)
        assert xp.all(xp.isnan(tf.as_matrix()))
    else:
        with pytest.raises(ValueError):
            RigidTransform.from_matrix(invalid)

