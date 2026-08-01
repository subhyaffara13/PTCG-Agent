
def test_gh20048():
    # gh-20048 reported an infinite loop in _drv2_ppfsingle
    # check that the one identified is resolved
    class test_dist_gen(stats.rv_discrete):
        def _cdf(self, k):
            return min(k / 100, 0.99)

    test_dist = test_dist_gen(b=np.inf)

    message = "Arguments that bracket..."
    with pytest.raises(RuntimeError, match=message):
        test_dist.ppf(0.999)

