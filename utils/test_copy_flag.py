
def test_copy_flag(xp):
    # Test that copy=True creates new memory
    matrix = xp.eye(4)
    tf = RigidTransform(matrix, normalize=False, copy=True)
    matrix[0, 0] = 2
    assert tf.as_matrix()[0, 0] == 1

    # Test that copy=False shares memory
    matrix = xp.eye(4)
    tf = RigidTransform(matrix, normalize=False, copy=False)
    matrix[0, 0] = 2
    assert tf.as_matrix()[0, 0] == 2

