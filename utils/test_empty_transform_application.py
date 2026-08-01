
def test_empty_transform_application(xp):
    tf = RigidTransform.from_matrix(xp.empty((0, 4, 4)))

    assert tf.apply(xp.zeros((3,))).shape == (0, 3)
    assert tf.apply(xp.empty((0, 3))).shape == (0, 3)

    with pytest.raises(ValueError, match="operands could not be broadcast together"):
        tf.apply(xp.zeros((2, 3)))

