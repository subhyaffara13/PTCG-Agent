
def test_concatenate_validation(xp):
    tf = RigidTransform.from_matrix(xp.eye(4))

    # Test invalid inputs
    with pytest.raises(TypeError,
                       match="input must contain RigidTransform objects"):
        RigidTransform.concatenate([tf, xp.eye(4)])

    # Test incompatible shapes
    tf2 = RigidTransform.from_translation(xp.ones((1, 1, 1, 3)))
    # Frameworks have a highly heterogeneous way of reporting errors for this case
    with pytest.raises((ValueError, TypeError, RuntimeError)):
        RigidTransform.concatenate([tf, tf2])

