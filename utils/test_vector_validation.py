
def test_vector_validation(xp):
    tf = rigid_transform_to_xp(RigidTransform.identity(2), xp=xp)

    # Test invalid vector shapes
    with pytest.raises(ValueError, match="Expected vector to have shape"):
        tf.apply(xp.asarray([1, 2]))

    with pytest.raises(ValueError, match="Expected vector to have shape"):
        tf.apply(xp.zeros((2, 2)))

    with pytest.raises(ValueError, match="operands could not be broadcast"):
        tf.apply(xp.zeros((1, 4, 3)))

