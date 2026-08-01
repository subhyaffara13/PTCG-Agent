
def test_issue_17473():
    x = Symbol('x')
    n = Symbol('n')
    h = S.Half
    ans = x**(n + 1)*gamma(h + h/n)*hyper((h + h/n,),
        (3*h, 3*h + h/n), -x**(2*n)/4)/(2*n*gamma(3*h + h/n))
    got = integrate(sin(x**n), x)
    assert got == ans
    _x = Symbol('x', zero=False)
    reps = {x: _x}
    assert integrate(sin(_x**n), _x) == ans.xreplace(reps).expand()

