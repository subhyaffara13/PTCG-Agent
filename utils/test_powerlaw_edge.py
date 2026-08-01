
def test_powerlaw_edge():
    # Regression test for gh-3986.
    p = stats.powerlaw.logpdf(0, 1)
    assert_equal(p, 0.0)

