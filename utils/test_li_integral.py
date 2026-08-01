
def test_li_integral():
    y = Symbol('y')
    assert Integral(li(y*x**2), x).doit() == Piecewise((x*li(x**2*y) - \
        x*Ei(3*log(x**2*y)/2)/sqrt(x**2*y),
        Ne(y, 0)), (0, True))

