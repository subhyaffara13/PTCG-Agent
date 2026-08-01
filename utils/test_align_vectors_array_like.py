
def test_align_vectors_array_like():
    rng = np.random.default_rng(123)
    c = Rotation.random(rng=rng)
    b = rng.normal(size=(5, 3))
    a = c.apply(b)

    est_expected, rssd_expected = Rotation.align_vectors(a, b)
    est, rssd = Rotation.align_vectors(a.tolist(), b.tolist())
    xp_assert_close(est_expected.as_quat(), est.as_quat())
    xp_assert_close(rssd, rssd_expected)

