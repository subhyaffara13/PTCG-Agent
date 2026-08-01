
def test_from_rotation(xp, ndim: int):
    atol = 1e-12
    rng = np.random.default_rng(0)
    shape = (ndim,) * (ndim - 1) + (4,)
    r = rotation_to_xp(Rotation.from_quat(rng.normal(size=shape)), xp=xp)
    tf = RigidTransform.from_rotation(r)
    xp_assert_close(tf.as_matrix()[..., :3, :3], r.as_matrix(), atol=atol)
    xp_assert_close(tf.as_matrix()[..., :3, 3], xp.zeros(shape[:-1] + (3,)), atol=atol)
    xp_assert_close(tf.as_matrix()[..., 3, :3], xp.zeros(shape[:-1] + (3,)), atol=atol)
    xp_assert_close(tf.as_matrix()[..., 3, 3], xp.ones(shape[:-1]), atol=atol)
    assert tf.single == (ndim == 1)

