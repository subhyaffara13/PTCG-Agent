import random

def test_linspace(Poly):
    d = Poly.domain + random((2,)) * .25
    w = Poly.window + random((2,)) * .25
    p = Poly([1, 2, 3], domain=d, window=w)
    # check default domain
    xtgt = np.linspace(d[0], d[1], 20)
    ytgt = p(xtgt)
    xres, yres = p.linspace(20)
    assert_almost_equal(xres, xtgt)
    assert_almost_equal(yres, ytgt)
    # check specified domain
    xtgt = np.linspace(0, 2, 20)
    ytgt = p(xtgt)
    xres, yres = p.linspace(20, domain=[0, 2])
    assert_almost_equal(xres, xtgt)
    assert_almost_equal(yres, ytgt)


def test_linspace():
    assert linspace(2, 9, 7) == [mpf('2.0'), mpf('3.166666666666667'),
        mpf('4.3333333333333339'), mpf('5.5'), mpf('6.666666666666667'),
        mpf('7.8333333333333339'), mpf('9.0')]
    assert linspace(2, 9, 7, endpoint=0) == [mpf('2.0'), mpf('3.0'), mpf('4.0'),
        mpf('5.0'), mpf('6.0'), mpf('7.0'), mpf('8.0')]
    assert linspace(2, 7, 1) == [mpf(2)]

