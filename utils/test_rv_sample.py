
def test_rv_sample():
    # Thoroughly test rv_sample and check that gh-3758 is resolved

    # Generate a random discrete distribution
    rng = np.random.default_rng(98430143469)
    xk = np.sort(rng.random(10) * 10)
    pk = rng.random(10)
    pk /= np.sum(pk)
    dist = stats.rv_discrete(values=(xk, pk))

    # Generate points to the left and right of xk
    xk_left = (np.array([0] + xk[:-1].tolist()) + xk)/2
    xk_right = (np.array(xk[1:].tolist() + [xk[-1]+1]) + xk)/2

    # Generate points to the left and right of cdf
    cdf2 = np.cumsum(pk)
    cdf2_left = (np.array([0] + cdf2[:-1].tolist()) + cdf2)/2
    cdf2_right = (np.array(cdf2[1:].tolist() + [1]) + cdf2)/2

    # support - leftmost and rightmost xk
    a, b = dist.support()
    assert_allclose(a, xk[0])
    assert_allclose(b, xk[-1])

    # pmf - supported only on the xk
    assert_allclose(dist.pmf(xk), pk)
    assert_allclose(dist.pmf(xk_right), 0)
    assert_allclose(dist.pmf(xk_left), 0)

    # logpmf is log of the pmf; log(0) = -np.inf
    with np.errstate(divide='ignore'):
        assert_allclose(dist.logpmf(xk), np.log(pk))
        assert_allclose(dist.logpmf(xk_right), -np.inf)
        assert_allclose(dist.logpmf(xk_left), -np.inf)

    # cdf - the cumulative sum of the pmf
    assert_allclose(dist.cdf(xk), cdf2)
    assert_allclose(dist.cdf(xk_right), cdf2)
    assert_allclose(dist.cdf(xk_left), [0]+cdf2[:-1].tolist())

    with np.errstate(divide='ignore'):
        assert_allclose(dist.logcdf(xk), np.log(dist.cdf(xk)),
                        atol=1e-15)
        assert_allclose(dist.logcdf(xk_right), np.log(dist.cdf(xk_right)),
                        atol=1e-15)
        assert_allclose(dist.logcdf(xk_left), np.log(dist.cdf(xk_left)),
                        atol=1e-15)

    # sf is 1-cdf
    assert_allclose(dist.sf(xk), 1-dist.cdf(xk))
    assert_allclose(dist.sf(xk_right), 1-dist.cdf(xk_right))
    assert_allclose(dist.sf(xk_left), 1-dist.cdf(xk_left))

    with np.errstate(divide='ignore'):
        assert_allclose(dist.logsf(xk), np.log(dist.sf(xk)),
                        atol=1e-15)
        assert_allclose(dist.logsf(xk_right), np.log(dist.sf(xk_right)),
                        atol=1e-15)
        assert_allclose(dist.logsf(xk_left), np.log(dist.sf(xk_left)),
                        atol=1e-15)

    # ppf
    assert_allclose(dist.ppf(cdf2), xk)
    assert_allclose(dist.ppf(cdf2_left), xk)
    assert_allclose(dist.ppf(cdf2_right)[:-1], xk[1:])
    assert_allclose(dist.ppf(0), a - 1)
    assert_allclose(dist.ppf(1), b)

    # isf
    sf2 = dist.sf(xk)
    assert_allclose(dist.isf(sf2), xk)
    assert_allclose(dist.isf(1-cdf2_left), dist.ppf(cdf2_left))
    assert_allclose(dist.isf(1-cdf2_right), dist.ppf(cdf2_right))
    assert_allclose(dist.isf(0), b)
    assert_allclose(dist.isf(1), a - 1)

    # interval is (ppf(alpha/2), isf(alpha/2))
    ps = np.linspace(0.01, 0.99, 10)
    int2 = dist.ppf(ps/2), dist.isf(ps/2)
    assert_allclose(dist.interval(1-ps), int2)
    assert_allclose(dist.interval(0), dist.median())
    assert_allclose(dist.interval(1), (a-1, b))

    # median is simply ppf(0.5)
    med2 = dist.ppf(0.5)
    assert_allclose(dist.median(), med2)

    # all four stats (mean, var, skew, and kurtosis) from the definitions
    mean2 = np.sum(xk*pk)
    var2 = np.sum((xk - mean2)**2 * pk)
    skew2 = np.sum((xk - mean2)**3 * pk) / var2**(3/2)
    kurt2 = np.sum((xk - mean2)**4 * pk) / var2**2 - 3
    assert_allclose(dist.mean(), mean2)
    assert_allclose(dist.std(), np.sqrt(var2))
    assert_allclose(dist.var(), var2)
    assert_allclose(dist.stats(moments='mvsk'), (mean2, var2, skew2, kurt2))

    # noncentral moment against definition
    mom3 = np.sum((xk**3) * pk)
    assert_allclose(dist.moment(3), mom3)

    # expect - check against moments
    assert_allclose(dist.expect(lambda x: 1), 1)
    assert_allclose(dist.expect(), mean2)
    assert_allclose(dist.expect(lambda x: x**3), mom3)

    # entropy is the negative of the expected value of log(p)
    with np.errstate(divide='ignore'):
        assert_allclose(-dist.expect(lambda x: dist.logpmf(x)), dist.entropy())

    # RVS is just ppf of uniform random variates
    rng = np.random.default_rng(98430143469)
    rvs = dist.rvs(size=100, random_state=rng)
    rng = np.random.default_rng(98430143469)
    rvs0 = dist.ppf(rng.random(size=100))
    assert_allclose(rvs, rvs0)

