
def test_collect_D_0():
    D = Derivative
    f = Function('f')
    x, a, b = symbols('x,a,b')
    fxx = D(f(x), x, x)

    assert collect(a*fxx + b*fxx, fxx) == (a + b)*fxx

