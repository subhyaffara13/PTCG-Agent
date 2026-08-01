
def test_empty_transform_inv_and_pow(xp):
    tf = RigidTransform.from_matrix(xp.empty((0, 4, 4)))
    assert len(tf.inv()) == 0
    assert len(tf ** 0) == 0
    assert len(tf ** 1) == 0
    assert len(tf ** -1) == 0
    assert len(tf ** 0.5) == 0

