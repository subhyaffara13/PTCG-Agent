
def test_setitem_fancy_indexing(xp):
    double = RigidTransform.from_translation(xp.asarray([[2, 2, 2], [3, 3, 3]]))
    tf = RigidTransform.from_translation(xp.asarray([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    idx = xp.asarray([0, 2])
    tf[idx] = double
    xp_assert_close(tf.translation, xp.asarray([[2.0, 2, 2], [4, 5, 6], [3, 3, 3]]))

