
def test_lomax_accuracy():
    # regression test for gh-4033
    p = stats.lomax.ppf(stats.lomax.cdf(1e-100, 1), 1)
    assert_allclose(p, 1e-100)

