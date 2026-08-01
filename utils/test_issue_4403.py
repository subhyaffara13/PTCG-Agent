
def test_issue_4403():
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z', positive=True)
    assert integrate(sqrt(x**2 + z**2), x) == \
        z**2*asinh(x/z)/2 + x*sqrt(x**2 + z**2)/2
    assert integrate(sqrt(x**2 - z**2), x) == \
        x*sqrt(x**2 - z**2)/2 - z**2*log(x + sqrt(x**2 - z**2))/2

    x = Symbol('x', real=True)
    y = Symbol('y', positive=True)
    assert integrate(1/(x**2 + y**2)**S('3/2'), x) == \
        x/(y**2*sqrt(x**2 + y**2))

