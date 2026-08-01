
def test_indexing_array_like():
    atol = 1e-12

    r = Rotation.from_euler('zyx', np.array([[90, 0, 0], [0, 90, 0]]), degrees=True)
    t = np.array([[1.0, 2, 3], [4, 5, 6]])
    tf = RigidTransform.from_components(t, r)

    tf_masked = tf[[False, True]]
    xp_assert_close(tf_masked.as_matrix()[:, :3, :3], r[[False, True]].as_matrix(),
                    atol=atol)
    xp_assert_close(tf_masked.as_matrix()[:, :3, 3], t[[False, True]], atol=atol)
    tf_masked = tf[[False, False]]
    assert len(tf_masked) == 0

