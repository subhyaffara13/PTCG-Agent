
def test_empty_transform_composition(xp):
    tf_empty = RigidTransform.from_matrix(xp.empty((0, 4, 4)))
    tf_single = RigidTransform.from_matrix(xp.eye(4))
    tf_many = rigid_transform_to_xp(RigidTransform.identity(3), xp=xp)

    assert len(tf_empty * tf_empty) == 0
    assert len(tf_empty * tf_single) == 0
    assert len(tf_single * tf_empty) == 0

    with pytest.raises(ValueError, match="Cannot broadcast"):
        tf_many * tf_empty

    with pytest.raises(ValueError, match="Cannot broadcast"):
        tf_empty * tf_many

