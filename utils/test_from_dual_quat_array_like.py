
def test_from_dual_quat_array_like():
    rng = np.random.default_rng(123)
    # Test single transform
    t = np.array([1, 2, 3])
    r = Rotation.random(rng=rng)
    tf_expected = RigidTransform.from_components(t, r)
    dual_quat = tf_expected.as_dual_quat().tolist()
    assert isinstance(dual_quat, list)
    tf = RigidTransform.from_dual_quat(dual_quat)
    xp_assert_close(tf.as_matrix(), tf_expected.as_matrix(), atol=1e-12)

    # Test multiple transforms
    t = [[1, 2, 3], [4, 5, 6]]
    r = Rotation.random(len(t), rng=rng)
    tf_expected = RigidTransform.from_components(t, r)
    dual_quat = tf_expected.as_dual_quat().tolist()
    assert isinstance(dual_quat, list)
    tf = RigidTransform.from_dual_quat(dual_quat)
    xp_assert_close(tf.as_matrix(), tf_expected.as_matrix(), atol=1e-12)

