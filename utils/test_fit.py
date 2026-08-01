
def test_fit(Poly):

    def f(x):
        return x * (x - 1) * (x - 2)
    x = np.linspace(0, 3)
    y = f(x)

    # check default value of domain and window
    p = Poly.fit(x, y, 3)
    assert_almost_equal(p.domain, [0, 3])
    assert_almost_equal(p(x), y)
    assert_equal(p.degree(), 3)

    # check with given domains and window
    d = Poly.domain + random((2,)) * .25
    w = Poly.window + random((2,)) * .25
    p = Poly.fit(x, y, 3, domain=d, window=w)
    assert_almost_equal(p(x), y)
    assert_almost_equal(p.domain, d)
    assert_almost_equal(p.window, w)
    p = Poly.fit(x, y, [0, 1, 2, 3], domain=d, window=w)
    assert_almost_equal(p(x), y)
    assert_almost_equal(p.domain, d)
    assert_almost_equal(p.window, w)

    # check with class domain default
    p = Poly.fit(x, y, 3, [])
    assert_equal(p.domain, Poly.domain)
    assert_equal(p.window, Poly.window)
    p = Poly.fit(x, y, [0, 1, 2, 3], [])
    assert_equal(p.domain, Poly.domain)
    assert_equal(p.window, Poly.window)

    # check that fit accepts weights.
    w = np.zeros_like(x)
    z = y + random(y.shape) * .25
    w[::2] = 1
    p1 = Poly.fit(x[::2], z[::2], 3)
    p2 = Poly.fit(x, z, 3, w=w)
    p3 = Poly.fit(x, z, [0, 1, 2, 3], w=w)
    assert_almost_equal(p1(x), p2(x))
    assert_almost_equal(p2(x), p3(x))


def test_fit():
    x, y = (range(10),) * 2
    p = poly.Polynomial.fit(x, y, deg=1, symbol='z')
    assert_equal(p.symbol, 'z')

