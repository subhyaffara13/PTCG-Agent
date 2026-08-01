
def test_ellip_harm_2():

    def I1(h2, k2, s):
        res = (ellip_harm_2(h2, k2, 1, 1, s)/(3 * ellip_harm(h2, k2, 1, 1, s))
        + ellip_harm_2(h2, k2, 1, 2, s)/(3 * ellip_harm(h2, k2, 1, 2, s)) +
        ellip_harm_2(h2, k2, 1, 3, s)/(3 * ellip_harm(h2, k2, 1, 3, s)))
        return res

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", "The occurrence of roundoff error", IntegrationWarning)
        assert_allclose(I1(5, 8, 10), 1/(10*sqrt((100-5)*(100-8))),
                        atol=1.5e-7, rtol=0)

        # Values produced by code from arXiv:1204.0267
        assert_allclose(ellip_harm_2(5, 8, 2, 1, 10), 0.00108056853382,
                        atol=1.5e-7, rtol=0)
        assert_allclose(ellip_harm_2(5, 8, 2, 2, 10), 0.00105820513809,
                        atol=1.5e-7, rtol=0)
        assert_allclose(ellip_harm_2(5, 8, 2, 3, 10), 0.00106058384743,
                        atol=1.5e-7, rtol=0)
        assert_allclose(ellip_harm_2(5, 8, 2, 4, 10), 0.00106774492306,
                        atol=1.5e-7, rtol=0)
        assert_allclose(ellip_harm_2(5, 8, 2, 5, 10), 0.00107976356454,
                        atol=1.5e-7, rtol=0)

