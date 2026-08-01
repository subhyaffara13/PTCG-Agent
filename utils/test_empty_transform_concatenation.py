
def test_empty_transform_concatenation(xp):
    tf_empty = RigidTransform.from_matrix(xp.empty((0, 4, 4)))
    tf_single = RigidTransform.from_matrix(xp.eye(4))
    tf_many = rigid_transform_to_xp(RigidTransform.identity(2), xp=xp)

    assert len(RigidTransform.concatenate([tf_empty, tf_empty])) == 0
    assert len(RigidTransform.concatenate([tf_empty, tf_single])) == 1
    assert len(RigidTransform.concatenate([tf_single, tf_empty])) == 1
    assert len(RigidTransform.concatenate([tf_empty, tf_many])) == 2
    assert len(RigidTransform.concatenate([tf_many, tf_empty])) == 2
    assert len(RigidTransform.concatenate([tf_many, tf_empty, tf_single])) == 3

