
def test_issue_3449():
    x = Symbol("x")
    assert sqrt(x - 1).subs(x, 5) == 2


def test_issue_3449():
    #test if powers are simplified correctly
    #see also issue 3995
    assert ((x**Rational(1, 3))**Rational(2)) == x**Rational(2, 3)
    assert (
        (x**Rational(3))**Rational(2, 5)) == (x**Rational(3))**Rational(2, 5)

    a = Symbol('a', real=True)
    b = Symbol('b', real=True)
    assert (a**2)**b == (abs(a)**b)**2
    assert sqrt(1/a) != 1/sqrt(a)  # e.g. for a = -1
    assert (a**3)**Rational(1, 3) != a
    assert (x**a)**b != x**(a*b)  # e.g. x = -1, a=2, b=1/2
    assert (x**.5)**b == x**(.5*b)
    assert (x**.5)**.5 == x**.25
    assert (x**2.5)**.5 != x**1.25  # e.g. for x = 5*I

    k = Symbol('k', integer=True)
    m = Symbol('m', integer=True)
    assert (x**k)**m == x**(k*m)
    assert Number(5)**Rational(2, 3) == Number(25)**Rational(1, 3)

    assert (x**.5)**2 == x**1.0
    assert (x**2)**k == (x**k)**2 == x**(2*k)

    a = Symbol('a', positive=True)
    assert (a**3)**Rational(2, 5) == a**Rational(6, 5)
    assert (a**2)**b == (a**b)**2
    assert (a**Rational(2, 3))**x == a**(x*Rational(2, 3)) != (a**x)**Rational(2, 3)

