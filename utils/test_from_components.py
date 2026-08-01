
def test_from_components(xp, r_ndim: int, t_ndim: int):
    atol = 1e-12
    dims = (6, 5, 4, 3)  # Common shape
    q_shape = dims[:r_ndim - 1][::-1] + (4,)
    t_shape = dims[:t_ndim - 1][::-1] + (3,)
    tf_shape = np.broadcast_shapes(q_shape[:-1], t_shape[:-1]) + (4, 4)
    rng = np.random.default_rng(0)

    t = xp.reshape(xp.arange(np.prod(t_shape[:-1]) * 3), t_shape)
    r = rotation_to_xp(Rotation.from_quat(rng.random(size=q_shape)), xp=xp)
    tf = RigidTransform.from_components(t, r)

    expected = xp.zeros(tf_shape)
    expected = xpx.at(expected)[..., :3, :3].set(r.as_matrix())
    t_float = xp_promote(t, force_floating=True, xp=xp)
    expected = xpx.at(expected)[..., :3, 3].set(t_float)
    expected = xpx.at(expected)[..., 3, 3].set(1)
    xp_assert_close(tf.as_matrix(), expected, atol=atol)
    assert tf.single == (r_ndim == 1 and t_ndim == 1)

