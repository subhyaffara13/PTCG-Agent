
def test_from_translation(xp, ndim: int):
    shape = (ndim,) * (ndim - 1)
    t = xp.reshape(xp.arange(ndim ** (ndim-1) * 3), shape + (3,))
    tf = RigidTransform.from_translation(t)

    expected = xp.tile(xp.eye(4), shape + (1, 1))
    t_float = xp_promote(t, force_floating=True, xp=xp)
    expected = xpx.at(expected)[..., :3, 3].set(t_float)
    xp_assert_close(tf.as_matrix(), expected)
    assert tf.single == (ndim == 1)

