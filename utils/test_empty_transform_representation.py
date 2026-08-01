
def test_empty_transform_representation(xp):
    tf = RigidTransform.from_matrix(xp.empty((0, 4, 4)))

    assert len(tf.rotation) == 0
    assert tf.translation.shape == (0, 3)

    t, r = tf.as_components()
    assert t.shape == (0, 3)
    assert len(r) == 0

    assert tf.as_matrix().shape == (0, 4, 4)
    assert tf.as_exp_coords().shape == (0, 6)
    assert tf.as_dual_quat().shape == (0, 8)

