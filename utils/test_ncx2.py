
def test_ncx2():
    """
    Test fitting the shape parameters (df, ncp) of ncx2 to mixed data.

    Calculation in R, with
    * 5 not censored values [2.7, 0.2, 6.5, 0.4, 0.1],
    * 1 interval-censored value [[0.6, 1.0]], and
    * 2 right-censored values [8, 8].

    > library(fitdistrplus)
    > data <- data.frame(left=c(2.7, 0.2, 6.5, 0.4, 0.1, 0.6, 8, 8),
    +                    right=c(2.7, 0.2, 6.5, 0.4, 0.1, 1.0, NA, NA))
    > result = fitdistcens(data, 'chisq', control=list(reltol=1e-14),
    +                      start=list(df=1, ncp=2))
    > result
    Fitting of the distribution ' chisq ' on censored data by maximum
    likelihood
    Parameters:
        estimate
    df  1.052871
    ncp 2.362934
    """
    data = CensoredData(uncensored=[2.7, 0.2, 6.5, 0.4, 0.1], right=[8, 8],
                        interval=[[0.6, 1.0]])
    with np.errstate(over='ignore'):  # remove context when gh-14901 is closed
        df, ncp, loc, scale = ncx2.fit(data, floc=0, fscale=1,
                                       optimizer=optimizer)
    assert_allclose(df, 1.052871, rtol=5e-6)
    assert_allclose(ncp, 2.362934, rtol=5e-6)
    assert loc == 0
    assert scale == 1

