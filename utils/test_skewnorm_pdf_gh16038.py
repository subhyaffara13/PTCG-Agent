
def test_skewnorm_pdf_gh16038():
    rng = np.random.default_rng(0)
    x, a = -np.inf, 0
    npt.assert_equal(stats.skewnorm.pdf(x, a), stats.norm.pdf(x))
    x, a = rng.random(size=(3, 3)), rng.random(size=(3, 3))
    mask = rng.random(size=(3, 3)) < 0.5
    a[mask] = 0
    x_norm = x[mask]
    res = stats.skewnorm.pdf(x, a)
    npt.assert_equal(res[mask], stats.norm.pdf(x_norm))
    npt.assert_equal(res[~mask], stats.skewnorm.pdf(x[~mask], a[~mask]))

