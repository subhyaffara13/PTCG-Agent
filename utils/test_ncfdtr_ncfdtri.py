
def test_ncfdtr_ncfdtri(dfn, dfd, nc, f, expected_cdf):
    # Reference values computed with mpmath with the following script
    #
    # import numpy as np
    #
    # from mpmath import mp
    # from scipy.special import ncfdtr
    #
    # mp.dps = 100
    #
    # def mp_ncfdtr(dfn, dfd, nc, f):
    #     # Uses formula 26.2.20 from Abramowitz and Stegun.
    #     dfn, dfd, nc, f = map(mp.mpf, (dfn, dfd, nc, f))
    #     def term(j):
    #         result = mp.exp(-nc/2)*(nc/2)**j / mp.factorial(j)
    #         result *= mp.betainc(
    #             dfn/2 + j, dfd/2, 0, f*dfn/(f*dfn + dfd), regularized=True
    #         )
    #         return result
    #     result = mp.nsum(term, [0, mp.inf])
    #     return float(result)
    #
    # dfn = np.logspace(-2, 2, 5)
    # dfd = np.logspace(-2, 2, 5)
    # nc = np.logspace(-2, 2, 5)
    # f = np.logspace(-2, 2, 5)
    #
    # dfn, dfd, nc, f = np.meshgrid(dfn, dfd, nc, f)
    # dfn, dfd, nc, f = map(np.ravel, (dfn, dfd, nc, f))
    #
    # cases = []
    # re = []
    # for x0, x1, x2, x3 in zip(*(dfn, dfd, nc, f)):
    #     observed = ncfdtr(x0, x1, x2, x3)
    #     expected = mp_ncfdtr(x0, x1, x2, x3)
    #     cases.append((x0, x1, x2, x3, expected))
    #     re.append((abs(expected - observed)/abs(expected)))
    #
    # assert np.max(re) < 1e-13
    #
    # rng = np.random.default_rng(1234)
    # sample_idx = rng.choice(len(re), replace=False, size=12)
    # cases = np.array(cases)[sample_idx].tolist()
    assert_allclose(sp.ncfdtr(dfn, dfd, nc, f), expected_cdf, rtol=1e-13, atol=0)
    # testing tails where the CDF reaches 0 or 1 does not make sense for inverses
    # of a CDF as they are not bijective in these regions
    if 0 < expected_cdf < 1:
        assert_allclose(sp.ncfdtri(dfn, dfd, nc, expected_cdf), f, rtol=5e-11)

