
def test_align_vectors_no_noise(xp):
    dtype = xpx.default_dtype(xp)
    atol = 1e-7 if dtype == xp.float64 else 2e-3
    rng = np.random.default_rng(14697284569885399755764481408308808739)
    c = rotation_to_xp(Rotation.random(rng=rng), xp)
    b = xp.asarray(rng.normal(size=(5, 3)), dtype=dtype)
    a = c.apply(b)

    est, rssd = Rotation.align_vectors(a, b)
    xp_assert_close(c.as_quat(), est.as_quat())
    xp_assert_close(rssd, xp.asarray(0.0)[()], check_shape=False, atol=atol)

