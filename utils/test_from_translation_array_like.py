
def test_from_translation_array_like():
    # Test single translation
    t = [1, 2, 3]
    tf = RigidTransform.from_translation(t)
    tf_expected = RigidTransform.from_translation(np.array(t))
    xp_assert_close(tf.as_matrix(), tf_expected.as_matrix())
    assert tf.single

    # Test multiple translations
    t = [[1, 2, 3], [4, 5, 6]]
    tf = RigidTransform.from_translation(t)
    tf_expected = RigidTransform.from_translation(np.array(t))
    xp_assert_close(tf.as_matrix(), tf_expected.as_matrix())
    assert not tf.single

