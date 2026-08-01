
def test_truncexpon_accuracy():
    # regression test for gh-4035
    p = stats.truncexpon.ppf(stats.truncexpon.cdf(1e-100, 1), 1)
    assert_allclose(p, 1e-100)

