
def test_invweibull_fit():
    """
    Test fitting invweibull to data.

    Here is a the same calculation in R:

    > library(evd)
    > library(fitdistrplus)
    > x = c(1, 1.25, 2, 2.5, 2.8,  3, 3.8, 4, 5, 8, 10, 12, 64, 99)
    > result = fitdist(x, 'frechet', control=list(reltol=1e-13),
    +                  fix.arg=list(loc=0), start=list(shape=2, scale=3))
    > result
    Fitting of the distribution ' frechet ' by maximum likelihood
    Parameters:
          estimate Std. Error
    shape 1.048482  0.2261815
    scale 3.099456  0.8292887
    Fixed parameters:
        value
    loc     0

    """

    def optimizer(func, x0, args=(), disp=0):
        return fmin(func, x0, args=args, disp=disp, xtol=1e-12, ftol=1e-12)

    x = np.array([1, 1.25, 2, 2.5, 2.8, 3, 3.8, 4, 5, 8, 10, 12, 64, 99])
    c, loc, scale = stats.invweibull.fit(x, floc=0, optimizer=optimizer)
    assert_allclose(c, 1.048482, rtol=5e-6)
    assert loc == 0
    assert_allclose(scale, 3.099456, rtol=5e-6)

