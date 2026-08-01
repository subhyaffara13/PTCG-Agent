
def test_skellam_gh11474():
    # test issue reported in gh-11474 caused by `cdfchn`
    mu = [1, 10, 100, 1000, 5000, 5050, 5100, 5250, 6000]
    cdf = skellam.cdf(0, mu, mu)
    # generated in R
    # library(skellam)
    # options(digits = 16)
    # mu = c(1, 10, 100, 1000, 5000, 5050, 5100, 5250, 6000)
    # pskellam(0, mu, mu, TRUE)
    cdf_expected = [0.6542541612768356, 0.5448901559424127, 0.5141135799745580,
                    0.5044605891382528, 0.5019947363350450, 0.5019848365953181,
                    0.5019750827993392, 0.5019466621805060, 0.5018209330219539]
    assert_allclose(cdf, cdf_expected)

