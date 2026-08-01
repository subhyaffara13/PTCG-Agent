
def test_composition(xp):
    atol = 1e-12
    tf_shapes = [(), (1,), (2,), (1, 2), (4, 2), (5, 4, 2)]
    dtype = xpx.default_dtype(xp)
    rng = np.random.default_rng(123)

    for tf_shape1, tf_shape2 in product(tf_shapes, repeat=2):
        # Random rotation and translation
        t1 = xp.asarray(rng.normal(size=tf_shape1 + (3,)))
        q1 = xp.asarray(rng.normal(size=tf_shape1 + (4,)))
        r1 = Rotation.from_quat(q1)
        tf1 = RigidTransform.from_components(t1, r1)

        t2 = xp.asarray(rng.normal(size=tf_shape2 + (3,)))
        q2 = xp.asarray(rng.normal(size=tf_shape2 + (4,)))
        r2 = Rotation.from_quat(q2)
        tf2 = RigidTransform.from_components(t2, r2)

        composed = tf2 * tf1
        vec = xp.asarray(rng.normal(size=(3,)), dtype=dtype)
        expected = tf2.apply(tf1.apply(vec))
        res = composed.apply(vec)
        assert res.shape == np.broadcast_shapes(tf_shape1, tf_shape2) + (3,)
        xp_assert_close(res, expected, atol=atol)

        expected = t2 + r2.apply(t1 + r1.apply(vec))
        xp_assert_close(composed.apply(vec), expected, atol=atol)
        assert composed.single == (tf1.single and tf2.single)


def test_composition():
    p = poly.Polynomial([3, 2, 1], symbol="t")
    q = poly.Polynomial([5, 1, 0, -1], symbol="λ_1")
    r = p(q)
    assert r.symbol == "λ_1"

