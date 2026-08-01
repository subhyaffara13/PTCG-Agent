
def test_regression_ticket_1421():
    assert_('pdf(x, mu, loc=0, scale=1)' not in stats.poisson.__doc__)
    assert_('pmf(x,' in stats.poisson.__doc__)

