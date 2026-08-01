
def test_nan_arguments_gh_issue_1362():
    with np.errstate(invalid='ignore'):
        assert_(np.isnan(stats.t.logcdf(1, np.nan)))
        assert_(np.isnan(stats.t.cdf(1, np.nan)))
        assert_(np.isnan(stats.t.logsf(1, np.nan)))
        assert_(np.isnan(stats.t.sf(1, np.nan)))
        assert_(np.isnan(stats.t.pdf(1, np.nan)))
        assert_(np.isnan(stats.t.logpdf(1, np.nan)))
        assert_(np.isnan(stats.t.ppf(1, np.nan)))
        assert_(np.isnan(stats.t.isf(1, np.nan)))

        assert_(np.isnan(stats.bernoulli.logcdf(np.nan, 0.5)))
        assert_(np.isnan(stats.bernoulli.cdf(np.nan, 0.5)))
        assert_(np.isnan(stats.bernoulli.logsf(np.nan, 0.5)))
        assert_(np.isnan(stats.bernoulli.sf(np.nan, 0.5)))
        assert_(np.isnan(stats.bernoulli.pmf(np.nan, 0.5)))
        assert_(np.isnan(stats.bernoulli.logpmf(np.nan, 0.5)))
        assert_(np.isnan(stats.bernoulli.ppf(np.nan, 0.5)))
        assert_(np.isnan(stats.bernoulli.isf(np.nan, 0.5)))

