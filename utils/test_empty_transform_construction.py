
def test_empty_transform_construction(xp):
    tf = RigidTransform.from_matrix(xp.empty((0, 4, 4)))
    assert len(tf) == 0
    assert not tf.single

    tf = RigidTransform.from_rotation(Rotation.from_quat(xp.zeros((0, 4))))
    assert len(tf) == 0
    assert not tf.single

    tf = RigidTransform.from_translation(xp.empty((0, 3)))
    assert len(tf) == 0
    assert not tf.single

    empty_rot = Rotation.from_quat(xp.zeros((0, 4)))
    tf = RigidTransform.from_components(xp.empty((0, 3)), empty_rot)
    assert len(tf) == 0
    assert not tf.single

    tf = RigidTransform.from_exp_coords(xp.empty((0, 6)))
    assert len(tf) == 0
    assert not tf.single

    tf = RigidTransform.from_dual_quat(xp.empty((0, 8)))
    assert len(tf) == 0
    assert not tf.single

    tf = RigidTransform.identity(0)
    assert len(tf) == 0
    assert not tf.single

