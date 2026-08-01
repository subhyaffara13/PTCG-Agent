
def test_powerlaw_stats():
    """Test the powerlaw stats function.

    This unit test is also a regression test for ticket 1548.

    The exact values are:
    mean:
        mu = a / (a + 1)
    variance:
        sigma**2 = a / ((a + 2) * (a + 1) ** 2)
    skewness:
        One formula (see https://en.wikipedia.org/wiki/Skewness) is
            gamma_1 = (E[X**3] - 3*mu*E[X**2] + 2*mu**3) / sigma**3
        A short calculation shows that E[X**k] is a / (a + k), so gamma_1
        can be implemented as
            n = a/(a+3) - 3*(a/(a+1))*a/(a+2) + 2*(a/(a+1))**3
            d = sqrt(a/((a+2)*(a+1)**2)) ** 3
            gamma_1 = n/d
        Either by simplifying, or by a direct calculation of mu_3 / sigma**3,
        one gets the more concise formula:
            gamma_1 = -2.0 * ((a - 1) / (a + 3)) * sqrt((a + 2) / a)
    kurtosis: (See https://en.wikipedia.org/wiki/Kurtosis)
        The excess kurtosis is
            gamma_2 = mu_4 / sigma**4 - 3
        A bit of calculus and algebra (sympy helps) shows that
            mu_4 = 3*a*(3*a**2 - a + 2) / ((a+1)**4 * (a+2) * (a+3) * (a+4))
        so
            gamma_2 = 3*(3*a**2 - a + 2) * (a+2) / (a*(a+3)*(a+4)) - 3
        which can be rearranged to
            gamma_2 = 6 * (a**3 - a**2 - 6*a + 2) / (a*(a+3)*(a+4))
    """
    cases = [(1.0, (0.5, 1./12, 0.0, -1.2)),
             (2.0, (2./3, 2./36, -0.56568542494924734, -0.6))]
    for a, exact_mvsk in cases:
        mvsk = stats.powerlaw.stats(a, moments="mvsk")
        assert_array_almost_equal(mvsk, exact_mvsk)

