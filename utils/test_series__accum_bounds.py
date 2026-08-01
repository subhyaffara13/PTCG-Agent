
def test_series_AccumBounds():
    assert limit(sin(k) - sin(k + 1), k, oo) == AccumBounds(-2, 2)
    assert limit(cos(k) - cos(k + 1) + 1, k, oo) == AccumBounds(-1, 3)

    # not the exact bound
    assert limit(sin(k) - sin(k)*cos(k), k, oo) == AccumBounds(-2, 2)

    # test for issue #9934
    lo = (-3 + cos(1))/2
    hi = (1 + cos(1))/2
    t1 = Mul(AccumBounds(lo, hi), 1/(-1 + cos(1)), evaluate=False)
    assert limit(simplify(Sum(cos(n).rewrite(exp), (n, 0, k)).doit().rewrite(sin)), k, oo) == t1

    t2 = Mul(AccumBounds(-1 + sin(1)/2, sin(1)/2 + 1), 1/(1 - cos(1)))
    assert limit(simplify(Sum(sin(n).rewrite(exp), (n, 0, k)).doit().rewrite(sin)), k, oo) == t2

    assert limit(((sin(x) + 1)/2)**x, x, oo) == AccumBounds(0, oo)  # wolfram says 0

    # https://github.com/sympy/sympy/issues/12312
    e = 2**(-x)*(sin(x) + 1)**x
    assert limit(e, x, oo) == AccumBounds(0, oo)

