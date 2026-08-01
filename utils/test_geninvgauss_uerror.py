
def test_geninvgauss_uerror():
    dist = stats.geninvgauss(3.2, 1.5)
    rng = FastGeneratorInversion(dist)
    err = rng.evaluate_error(size=10_000, random_state=67982)
    assert err[0] < 1e-10

