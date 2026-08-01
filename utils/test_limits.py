
def test_limits():
    k, x = symbols('k, x')
    assert hyper((1,), (Rational(4, 3), Rational(5, 3)), k**2).series(k) == \
           1 + 9*k**2/20 + 81*k**4/1120 + O(k**6) # issue 6350

    # https://github.com/sympy/sympy/issues/11465
    assert limit(1/hyper((1, ), (1, ), x), x, 0) == 1


def test_limits():
    mp.dps = 15
    assert limit(lambda x: (x-sin(x))/x**3, 0).ae(mpf(1)/6)
    assert limit(lambda n: (1+1/n)**n, inf).ae(e)

