
def test_normalize_dual_quaternion(xp, ndim: int):
    dtype = xpx.default_dtype(xp)
    atol = 1e-12 if dtype == xp.float64 else 1e-6
    rng = np.random.default_rng(100)
    shape = (ndim,) * (ndim - 1)

    dual_quat = normalize_dual_quaternion(xp.zeros((1, 8)))
    xp_assert_close(xp_vector_norm(dual_quat[0, :4], axis=-1), xp.asarray(1.0)[()],
                    atol=1e-12)
    xp_assert_close(xp.vecdot(dual_quat[0, :4], dual_quat[0, 4:])[()],
                    xp.asarray(0.0)[()], atol=1e-12)

    dual_quat = xp.asarray(rng.normal(size=shape + (8,)), dtype=dtype)
    dual_quat = normalize_dual_quaternion(dual_quat)
    expected = xp.ones(shape) if shape != () else xp.asarray(1.0)[()]
    xp_assert_close(xp_vector_norm(dual_quat[..., :4], axis=-1), expected, atol=atol)
    expected = xp.zeros(shape) if shape != () else xp.asarray(0.0)[()]
    vecdot = xp.vecdot(dual_quat[..., :4], dual_quat[..., 4:])
    vecdot = vecdot[()] if vecdot.shape == () else vecdot
    xp_assert_close(vecdot, expected, atol=atol)

