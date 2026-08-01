
def test_weibull_min_sas2():
    # http://support.sas.com/documentation/cdl/en/ormpug/67517/HTML/default/
    #      viewer.htm#ormpug_nlpsolver_examples06.htm

    # The last two values are right-censored.
    days = np.array([143, 164, 188, 188, 190, 192, 206, 209, 213, 216, 220,
                     227, 230, 234, 246, 265, 304, 216, 244])

    data = CensoredData.right_censored(days, [0]*(len(days) - 2) + [1]*2)

    c, loc, scale = weibull_min.fit(data, 1, loc=100, scale=100,
                                    optimizer=optimizer)

    assert_allclose(c, 2.7112, rtol=5e-4)
    assert_allclose(loc, 122.03, rtol=5e-4)
    assert_allclose(scale, 108.37, rtol=5e-4)

