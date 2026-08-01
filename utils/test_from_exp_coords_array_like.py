
def test_from_exp_coords_array_like():
    rng = np.random.default_rng(123)
    # Test single transform
    t = np.array([1, 2, 3])
    r = Rotation.random(rng=rng)
    tf_expected = RigidTransform.from_components(t, r)
    exp_coords = tf_expected.as_exp_coords().tolist()
    assert isinstance(exp_coords, list)
    tf = RigidTransform.from_exp_coords(exp_coords)
    xp_assert_close(tf.as_matrix(), tf_expected.as_matrix(), atol=1e-12)

    # Test multiple transforms
    t = [[1, 2, 3], [4, 5, 6]]
    r = Rotation.random(len(t), rng=rng)
    tf_expected = RigidTransform.from_components(t, r)
    exp_coords = tf_expected.as_exp_coords().tolist()
    assert isinstance(exp_coords, list)
    tf = RigidTransform.from_exp_coords(exp_coords)
    xp_assert_close(tf.as_matrix(), tf_expected.as_matrix(), atol=1e-12)

