
def test_setitem_validation(xp):
    tf = RigidTransform.from_translation(xp.asarray([[1, 2, 3], [4, 5, 6]]))
    single = RigidTransform.from_matrix(xp.eye(4))

    # Test setting item on single transform
    with pytest.raises(TypeError, match="Single transform is not subscriptable"):
        single[0] = tf

    # Test invalid value type
    with pytest.raises(TypeError, match="value must be a RigidTransform"):
        tf[0] = xp.eye(4)

