
def test_invgauss():
    """
    Fit just the shape parameter of invgauss to data with one value
    left-censored and one value right-censored.

    Calculation in R; using a fixed dispersion parameter amounts to fixing
    the scale to be 1.

    > library(statmod)
    > library(fitdistrplus)
    > left <- c(NA, 0.4813096, 0.5571880, 0.5132463, 0.3801414, 0.5904386,
    +           0.4822340, 0.3478597, 3, 0.7191797, 1.5810902, 0.4442299)
    > right <- c(0.15, 0.4813096, 0.5571880, 0.5132463, 0.3801414, 0.5904386,
    +            0.4822340, 0.3478597, NA, 0.7191797, 1.5810902, 0.4442299)
    > data <- data.frame(left=left, right=right)
    > result = fitdistcens(data, 'invgauss', control=list(reltol=1e-12),
    +                      fix.arg=list(dispersion=1), start=list(mean=3))
    > result
    Fitting of the distribution ' invgauss ' on censored data by maximum
      likelihood
    Parameters:
         estimate
    mean 0.853469
    Fixed parameters:
               value
    dispersion     1
    > result$sd
        mean
    0.247636

    Here's the R calculation with the dispersion as a free parameter to
    be fit.

    > result = fitdistcens(data, 'invgauss', control=list(reltol=1e-12),
    +                      start=list(mean=3, dispersion=1))
    > result
    Fitting of the distribution ' invgauss ' on censored data by maximum
    likelihood
    Parameters:
                estimate
    mean       0.8699819
    dispersion 1.2261362

    The parametrization of the inverse Gaussian distribution in the
    `statmod` package is not the same as in SciPy (see
        https://arxiv.org/abs/1603.06687
    for details).  The translation from R to SciPy is

        scale = 1/dispersion
        mu    = mean * dispersion

    > 1/result$estimate['dispersion']  # 1/dispersion
    dispersion
     0.8155701
    > result$estimate['mean'] * result$estimate['dispersion']
        mean
    1.066716

    Those last two values are the SciPy scale and shape parameters.
    """
    # One point is left-censored, and one is right-censored.
    x = [0.4813096, 0.5571880, 0.5132463, 0.3801414,
         0.5904386, 0.4822340, 0.3478597, 0.7191797,
         1.5810902, 0.4442299]
    data = CensoredData(uncensored=x, left=[0.15], right=[3])

    # Fit only the shape parameter.
    mu, loc, scale = invgauss.fit(data, floc=0, fscale=1, optimizer=optimizer)

    assert_allclose(mu, 0.853469, rtol=5e-5)
    assert loc == 0
    assert scale == 1

    # Fit the shape and scale.
    mu, loc, scale = invgauss.fit(data, floc=0, optimizer=optimizer)

    assert_allclose(mu, 1.066716, rtol=5e-5)
    assert loc == 0
    assert_allclose(scale, 0.8155701, rtol=5e-5)

