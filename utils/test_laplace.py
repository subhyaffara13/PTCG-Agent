
def test_laplace():
    mu = Symbol("mu")
    b = Symbol("b", positive=True)

    X = Laplace('x', mu, b)

    #Tests characteristic_function
    assert characteristic_function(X)(x) == (exp(I*mu*x)/(b**2*x**2 + 1))

    assert density(X)(x) == exp(-Abs(x - mu)/b)/(2*b)
    assert cdf(X)(x) == Piecewise((exp((-mu + x)/b)/2, mu > x),
                            (-exp((mu - x)/b)/2 + 1, True))
    X = Laplace('x', [1, 2], [[1, 0], [0, 1]])
    assert isinstance(pspace(X).distribution, MultivariateLaplaceDistribution)


def test_laplace():
    """
    Fir the Laplace distribution to left- and right-censored data.

    Calculation in R:

    > library(fitdistrplus)
    > dlaplace <- function(x, location=0, scale=1) {
    +     return(0.5*exp(-abs((x - location)/scale))/scale)
    + }
    > plaplace <- function(q, location=0, scale=1) {
    +     z <- (q - location)/scale
    +     s <- sign(z)
    +     f <- -s*0.5*exp(-abs(z)) + (s+1)/2
    +     return(f)
    + }
    > left <- c(NA, -41.564, 50.0, 15.7384, 50.0, 10.0452, -2.0684,
    +           -19.5399, 50.0,   9.0005, 27.1227, 4.3113, -3.7372,
    +           25.3111, 14.7987,  34.0887,  50.0, 42.8496, 18.5862,
    +           32.8921, 9.0448, -27.4591, NA, 19.5083, -9.7199)
    > right <- c(-50.0, -41.564,  NA, 15.7384, NA, 10.0452, -2.0684,
    +            -19.5399, NA, 9.0005, 27.1227, 4.3113, -3.7372,
    +            25.3111, 14.7987, 34.0887, NA,  42.8496, 18.5862,
    +            32.8921, 9.0448, -27.4591, -50.0, 19.5083, -9.7199)
    > data <- data.frame(left=left, right=right)
    > result <- fitdistcens(data, 'laplace', start=list(location=10, scale=10),
    +                       control=list(reltol=1e-13))
    > result
    Fitting of the distribution ' laplace ' on censored data by maximum
      likelihood
    Parameters:
             estimate
    location 14.79870
    scale    30.93601
    > result$sd
         location     scale
    0.1758864 7.0972125
    """
    # The value -50 is left-censored, and the value 50 is right-censored.
    obs = np.array([-50.0, -41.564, 50.0, 15.7384, 50.0, 10.0452, -2.0684,
                    -19.5399, 50.0, 9.0005, 27.1227, 4.3113, -3.7372,
                    25.3111, 14.7987, 34.0887, 50.0, 42.8496, 18.5862,
                    32.8921, 9.0448, -27.4591, -50.0, 19.5083, -9.7199])
    x = obs[(obs != -50.0) & (obs != 50)]
    left = obs[obs == -50.0]
    right = obs[obs == 50.0]
    data = CensoredData(uncensored=x, left=left, right=right)
    loc, scale = laplace.fit(data, loc=10, scale=10, optimizer=optimizer)
    assert_allclose(loc, 14.79870, rtol=5e-6)
    assert_allclose(scale, 30.93601, rtol=5e-6)

