
def test_inverse_apply(xp):
    atol = 1e-12
    # Broadcast shape: (6, 5, 4, 2) ( + (3,) for vectors, + (4,) for rotations)
    vector_shapes = [(), (1,), (2,), (1, 2), (5, 1, 2)]
    tf_shapes = [(), (1,), (2,), (1, 2), (4, 2), (1, 4, 2), (5, 4, 2), (6, 5, 4, 2)]
    rng = np.random.default_rng(123)

    for tf_shape, v_shape in product(tf_shapes, vector_shapes):
        # Random rotation and translation
        t = xp.asarray(rng.normal(size=tf_shape + (3,)))
        q = xp.asarray(rng.normal(size=tf_shape + (4,)))
        r = Rotation.from_quat(q)
        tf = RigidTransform.from_components(t, r)

        vecs = xp.asarray(rng.normal(size=v_shape + (3,)))
        expected = tf.inv().apply(vecs)
        res = tf.apply(vecs, inverse=True)
        assert res.shape == np.broadcast_shapes(tf_shape, v_shape) + (3,)
        xp_assert_close(res, expected, atol=atol)

