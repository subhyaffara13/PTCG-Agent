
def test_as_components(xp, ndim):
    dtype = xpx.default_dtype(xp)
    atol = 1e-12 if dtype == xp.float64 else 1e-6
    shape = (ndim,) * (ndim - 1)
    rng = np.random.default_rng(123)
    t = xp.asarray(rng.normal(size=shape + (3,)), dtype=dtype)
    r = rotation_to_xp(Rotation.from_quat(rng.random(shape + (4,))), xp=xp)
    tf = RigidTransform.from_components(t, r)
    new_t, new_r = tf.as_components()
    assert xp.all(new_r.approx_equal(r, atol=atol))
    xp_assert_close(new_t, t, atol=atol)

