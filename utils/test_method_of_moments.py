
def test_method_of_moments():
    # example from https://en.wikipedia.org/wiki/Method_of_moments_(statistics)
    x = [0, 0, 0, 0, 1]
    a = 1/5 - 2*np.sqrt(3)/5
    b = 1/5 + 2*np.sqrt(3)/5
    # force use of method of moments (uniform.fit is overridden)
    loc, scale = super(type(stats.uniform), stats.uniform).fit(x, method="MM")
    npt.assert_almost_equal(loc, a, decimal=4)
    npt.assert_almost_equal(loc+scale, b, decimal=4)

