
def test_issue_5223():
    assert series(1, x) == 1
    assert next(S.Zero.lseries(x)) == 0
    assert cos(x).series() == cos(x).series(x)
    raises(ValueError, lambda: cos(x + y).series())
    raises(ValueError, lambda: x.series(dir=""))

    assert (cos(x).series(x, 1) -
            cos(x + 1).series(x).subs(x, x - 1)).removeO() == 0
    e = cos(x).series(x, 1, n=None)
    assert [next(e) for i in range(2)] == [cos(1), -((x - 1)*sin(1))]
    e = cos(x).series(x, 1, n=None, dir='-')
    assert [next(e) for i in range(2)] == [cos(1), (1 - x)*sin(1)]
    # the following test is exact so no need for x -> x - 1 replacement
    assert abs(x).series(x, 1, dir='-') == x
    assert exp(x).series(x, 1, dir='-', n=3).removeO() == \
        E - E*(-x + 1) + E*(-x + 1)**2/2

    D = Derivative
    assert D(x**2 + x**3*y**2, x, 2, y, 1).series(x).doit() == 12*x*y
    assert next(D(cos(x), x).lseries()) == D(1, x)
    assert D(
        exp(x), x).series(n=3) == D(1, x) + D(x, x) + D(x**2/2, x) + D(x**3/6, x) + O(x**3)

    assert Integral(x, (x, 1, 3), (y, 1, x)).series(x) == -4 + 4*x

    assert (1 + x + O(x**2)).getn() == 2
    assert (1 + x).getn() is None

    raises(PoleError, lambda: ((1/sin(x))**oo).series())
    logx = Symbol('logx')
    assert ((sin(x))**y).nseries(x, n=1, logx=logx) == \
        exp(y*logx) + O(x*exp(y*logx), x)

    assert sin(1/x).series(x, oo, n=5) == 1/x - 1/(6*x**3) + O(x**(-5), (x, oo))
    assert abs(x).series(x, oo, n=5, dir='+') == x
    assert abs(x).series(x, -oo, n=5, dir='-') == -x
    assert abs(-x).series(x, oo, n=5, dir='+') == x
    assert abs(-x).series(x, -oo, n=5, dir='-') == -x

    assert exp(x*log(x)).series(n=3) == \
        1 + x*log(x) + x**2*log(x)**2/2 + O(x**3*log(x)**3)
    # XXX is this right? If not, fix "ngot > n" handling in expr.
    p = Symbol('p', positive=True)
    assert exp(sqrt(p)**3*log(p)).series(n=3) == \
        1 + p**S('3/2')*log(p) + O(p**3*log(p)**3)

    assert exp(sin(x)*log(x)).series(n=2) == 1 + x*log(x) + O(x**2*log(x)**2)

