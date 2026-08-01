
def test_powers():
    assert cse(x*y**2 + x*y) == ([(x0, x*y)], [x0*y + x0])


def test_powers():
    assert integrate(2**x + 3**x, x) == 2**x/log(2) + 3**x/log(3)


def test_powers():
    assert integer_nthroot(1, 2) == (1, True)
    assert integer_nthroot(1, 5) == (1, True)
    assert integer_nthroot(2, 1) == (2, True)
    assert integer_nthroot(2, 2) == (1, False)
    assert integer_nthroot(2, 5) == (1, False)
    assert integer_nthroot(4, 2) == (2, True)
    assert integer_nthroot(123**25, 25) == (123, True)
    assert integer_nthroot(123**25 + 1, 25) == (123, False)
    assert integer_nthroot(123**25 - 1, 25) == (122, False)
    assert integer_nthroot(1, 1) == (1, True)
    assert integer_nthroot(0, 1) == (0, True)
    assert integer_nthroot(0, 3) == (0, True)
    assert integer_nthroot(10000, 1) == (10000, True)
    assert integer_nthroot(4, 2) == (2, True)
    assert integer_nthroot(16, 2) == (4, True)
    assert integer_nthroot(26, 2) == (5, False)
    assert integer_nthroot(1234567**7, 7) == (1234567, True)
    assert integer_nthroot(1234567**7 + 1, 7) == (1234567, False)
    assert integer_nthroot(1234567**7 - 1, 7) == (1234566, False)
    b = 25**1000
    assert integer_nthroot(b, 1000) == (25, True)
    assert integer_nthroot(b + 1, 1000) == (25, False)
    assert integer_nthroot(b - 1, 1000) == (24, False)
    c = 10**400
    c2 = c**2
    assert integer_nthroot(c2, 2) == (c, True)
    assert integer_nthroot(c2 + 1, 2) == (c, False)
    assert integer_nthroot(c2 - 1, 2) == (c - 1, False)
    assert integer_nthroot(2, 10**10) == (1, False)

    p, r = integer_nthroot(int(factorial(10000)), 100)
    assert p % (10**10) == 5322420655
    assert not r

    # Test that this is fast
    assert integer_nthroot(2, 10**10) == (1, False)

    # output should be int if possible
    assert type(integer_nthroot(2**61, 2)[0]) is int


def test_powers():
    assert sqrt(1 - sqrt(x)).subs(x, 4) == I
    assert (sqrt(1 - x**2)**3).subs(x, 2) == - 3*I*sqrt(3)
    assert (x**Rational(1, 3)).subs(x, 27) == 3
    assert (x**Rational(1, 3)).subs(x, -27) == 3*(-1)**Rational(1, 3)
    assert ((-x)**Rational(1, 3)).subs(x, 27) == 3*(-1)**Rational(1, 3)
    n = Symbol('n', negative=True)
    assert (x**n).subs(x, 0) is S.ComplexInfinity
    assert exp(-1).subs(S.Exp1, 0) is S.ComplexInfinity
    assert (x**(4.0*y)).subs(x**(2.0*y), n) == n**2.0
    assert (2**(x + 2)).subs(2, 3) == 3**(x + 3)

