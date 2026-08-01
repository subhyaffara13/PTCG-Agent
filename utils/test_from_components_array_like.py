
def test_from_components_array_like():
    rng = np.random.default_rng(123)
    # Test single rotation and translation
    t = [1, 2, 3]
    r = Rotation.random(rng=rng)
    tf = RigidTransform.from_components(t, r)
    tf_expected = RigidTransform.from_components(np.array(t), r)
    xp_assert_close(tf.as_matrix(), tf_expected.as_matrix(), atol=1e-12)
    assert tf.single

    # Test multiple rotations and translations
    t = [[1, 2, 3], [4, 5, 6]]
    r = Rotation.random(len(t), rng=rng)
    tf = RigidTransform.from_components(t, r)
    tf_expected = RigidTransform.from_components(np.array(t), r)
    xp_assert_close(tf.as_matrix(), tf_expected.as_matrix(), atol=1e-12)
    assert not tf.single

