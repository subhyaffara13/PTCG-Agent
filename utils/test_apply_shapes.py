
def test_apply_shapes(xp):
    rng = np.random.default_rng(0)
    # Broadcast shape: (6, 5, 4, 2) ( + (3,) for vectors, + (4,) for rotations)
    vector_shapes = [(), (1,), (2,), (1, 2), (5, 1, 2)]
    rot_shapes = [(), (1,), (2,), (1, 2), (4, 2), (1, 4, 2), (5, 4, 2), (6, 5, 4, 2)]

    for q_shape, v_shape in product(rot_shapes, vector_shapes):
        v = xp.asarray(rng.normal(size=v_shape + (3,)))
        q = xp.asarray(rng.normal(size=q_shape + (4,)))
        r = Rotation.from_quat(q)
        shape = np.broadcast_shapes(q_shape, v_shape) + (3,)
        x = r.apply(v)
        assert x.shape == shape
        x = r.apply(v, inverse=True)
        assert x.shape == shape

