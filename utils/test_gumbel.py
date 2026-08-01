
def test_gumbel():
    beta = Symbol("beta", positive=True)
    mu = Symbol("mu")
    x = Symbol("x")
    y = Symbol("y")
    X = Gumbel("x", beta, mu)
    Y = Gumbel("y", beta, mu, minimum=True)
    assert density(X)(x).expand() == \
    exp(mu/beta)*exp(-x/beta)*exp(-exp(mu/beta)*exp(-x/beta))/beta
    assert density(Y)(y).expand() == \
    exp(-mu/beta)*exp(y/beta)*exp(-exp(-mu/beta)*exp(y/beta))/beta
    assert cdf(X)(x).expand() == \
    exp(-exp(mu/beta)*exp(-x/beta))
    assert characteristic_function(X)(x) == exp(I*mu*x)*gamma(-I*beta*x + 1)


def test_gumbel():
    """
    Fit gumbel_l and gumbel_r to censored data.

    This R calculation should match gumbel_r.

    > library(evd)
    > library(fitdistrplus)
    > data = data.frame(left=c(0, 2, 3, 9, 10, 10),
    +                   right=c(1, 2, 3, 9, NA, NA))
    > result = fitdistcens(data, 'gumbel',
    +                      control=list(reltol=1e-14),
    +                      start=list(loc=4, scale=5))
    > result
    Fitting of the distribution ' gumbel ' on censored data by maximum
    likelihood
    Parameters:
          estimate
    loc   4.487853
    scale 4.843640
    """
    # First value is interval-censored. Last two are right-censored.
    uncensored = np.array([2, 3, 9])
    right = np.array([10, 10])
    interval = np.array([[0, 1]])
    data = CensoredData(uncensored, right=right, interval=interval)
    loc, scale = gumbel_r.fit(data, optimizer=optimizer)
    assert_allclose(loc, 4.487853, rtol=5e-6)
    assert_allclose(scale, 4.843640, rtol=5e-6)

    # Negate the data and reverse the intervals, and test with gumbel_l.
    data2 = CensoredData(-uncensored, left=-right,
                         interval=-interval[:, ::-1])
    # Fitting gumbel_l to data2 should give the same result as above, but
    # with loc negated.
    loc2, scale2 = gumbel_l.fit(data2, optimizer=optimizer)
    assert_allclose(loc2, -4.487853, rtol=5e-6)
    assert_allclose(scale2, 4.843640, rtol=5e-6)

