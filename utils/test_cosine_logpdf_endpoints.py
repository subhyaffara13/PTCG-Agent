
def test_cosine_logpdf_endpoints():
    logp = stats.cosine.logpdf([-np.pi, np.pi])
    # reference value calculated using mpmath assuming `np.cos(-1)` is four
    # floating point numbers too high. See gh-18382.
    assert_array_less(logp, -37.18838327496655)

