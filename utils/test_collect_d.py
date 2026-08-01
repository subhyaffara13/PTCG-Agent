
def test_collect_D():
    D = Derivative
    f = Function('f')
    x, a, b = symbols('x,a,b')
    fx = D(f(x), x)
    fxx = D(f(x), x, x)

    assert collect(a*fx + b*fx, fx) == (a + b)*fx
    assert collect(a*D(fx, x) + b*D(fx, x), fx) == (a + b)*D(fx, x)
    assert collect(a*fxx + b*fxx, fx) == (a + b)*D(fx, x)
    # issue 4784
    assert collect(5*f(x) + 3*fx, fx) == 5*f(x) + 3*fx
    assert collect(f(x) + f(x)*diff(f(x), x) + x*diff(f(x), x)*f(x), f(x).diff(x)) == \
        (x*f(x) + f(x))*D(f(x), x) + f(x)
    assert collect(f(x) + f(x)*diff(f(x), x) + x*diff(f(x), x)*f(x), f(x).diff(x), exact=True) == \
        (x*f(x) + f(x))*D(f(x), x) + f(x)
    assert collect(1/f(x) + 1/f(x)*diff(f(x), x) + x*diff(f(x), x)/f(x), f(x).diff(x), exact=True) == \
        (1/f(x) + x/f(x))*D(f(x), x) + 1/f(x)
    e = (1 + x*fx + fx)/f(x)
    assert collect(e.expand(), fx) == fx*(x/f(x) + 1/f(x)) + 1/f(x)

