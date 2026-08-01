
def test_poisson_logpmf_ticket_1436():
    assert_(np.isfinite(stats.poisson.logpmf(1500, 200)))

