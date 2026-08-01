
def test_logistic():
    mu = Symbol("mu", real=True)
    s = Symbol("s", positive=True)
    p = Symbol("p", positive=True)

    X = Logistic('x', mu, s)

    #Tests characteristics_function
    assert characteristic_function(X)(x) == \
           (Piecewise((pi*s*x*exp(I*mu*x)/sinh(pi*s*x), Ne(x, 0)), (1, True)))

    assert density(X)(x) == exp((-x + mu)/s)/(s*(exp((-x + mu)/s) + 1)**2)
    assert cdf(X)(x) == 1/(exp((mu - x)/s) + 1)
    assert quantile(X)(p) == mu - s*log(-S.One + 1/p)


def test_logistic():
    """
    Fit the logistic distribution to left-censored data.

    Calculation in R:
    > library(fitdistrplus)
    > left = c(13.5401, 37.4235, 11.906 , 13.998 ,  NA    ,  0.4023,  NA    ,
    +          10.9044, 21.0629,  9.6985,  NA    , 12.9016, 39.164 , 34.6396,
    +          NA    , 20.3665, 16.5889, 18.0952, 45.3818, 35.3306,  8.4949,
    +          3.4041,  NA    ,  7.2828, 37.1265,  6.5969, 17.6868, 17.4977,
    +          16.3391, 36.0541)
    > right = c(13.5401, 37.4235, 11.906 , 13.998 ,  0.    ,  0.4023,  0.    ,
    +           10.9044, 21.0629,  9.6985,  0.    , 12.9016, 39.164 , 34.6396,
    +           0.    , 20.3665, 16.5889, 18.0952, 45.3818, 35.3306,  8.4949,
    +           3.4041,  0.    ,  7.2828, 37.1265,  6.5969, 17.6868, 17.4977,
    +           16.3391, 36.0541)
    > data = data.frame(left=left, right=right)
    > result = fitdistcens(data, 'logis', control=list(reltol=1e-14))
    > result
    Fitting of the distribution ' logis ' on censored data by maximum
      likelihood
    Parameters:
              estimate
    location 14.633459
    scale     9.232736
    > result$sd
    location    scale
    2.931505 1.546879
    """
    # Values that are zero are left-censored; the true values are less than 0.
    x = np.array([13.5401, 37.4235, 11.906, 13.998, 0.0, 0.4023, 0.0, 10.9044,
                  21.0629, 9.6985, 0.0, 12.9016, 39.164, 34.6396, 0.0, 20.3665,
                  16.5889, 18.0952, 45.3818, 35.3306, 8.4949, 3.4041, 0.0,
                  7.2828, 37.1265, 6.5969, 17.6868, 17.4977, 16.3391,
                  36.0541])
    data = CensoredData.left_censored(x, censored=(x == 0))
    loc, scale = logistic.fit(data, optimizer=optimizer)
    assert_allclose(loc, 14.633459, rtol=5e-7)
    assert_allclose(scale, 9.232736, rtol=5e-6)

