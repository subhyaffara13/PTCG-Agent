
def test_apply_array_like():
    rng = np.random.default_rng(123)
    # Single vector
    t = np.array([1, 2, 3])
    r = Rotation.random(rng=rng)
    tf = RigidTransform.from_components(t, r)
    vec = [1, 0, 0]
    expected = t + r.apply(vec)
    xp_assert_close(tf.apply(vec), expected, atol=1e-12)

    # Multiple vectors
    t = np.array([[1, 2, 3], [4, 5, 6]])
    r = Rotation.random(len(t), rng=rng)
    tf = RigidTransform.from_components(t, r)
    vec = [[1, 0, 0], [0, 1, 0]]
    expected = t + r.apply(vec)
    xp_assert_close(tf.apply(vec), expected, atol=1e-12)


def test_apply_array_like():
    rng = np.random.default_rng(123)
    # Single vector
    r = Rotation.random(rng=rng)
    t = rng.uniform(-100, 100, size=(3,))
    v = r.apply(t.tolist())
    v_expected = r.apply(t)
    xp_assert_close(v, v_expected, atol=1e-12)
    # Multiple vectors
    t = rng.uniform(-100, 100, size=(2, 3))
    v = r.apply(t.tolist())
    v_expected = r.apply(t)
    xp_assert_close(v, v_expected, atol=1e-12)

