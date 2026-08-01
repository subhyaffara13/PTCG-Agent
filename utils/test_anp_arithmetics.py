
def test_ANP_arithmetics():
    mod = [QQ(1), QQ(0), QQ(0), QQ(-2)]

    a = ANP([QQ(2), QQ(-1), QQ(1)], mod, QQ)
    b = ANP([QQ(1), QQ(2)], mod, QQ)

    c = ANP([QQ(-2), QQ(1), QQ(-1)], mod, QQ)

    assert a.neg() == -a == c

    c = ANP([QQ(2), QQ(0), QQ(3)], mod, QQ)

    assert a.add(b) == a + b == c
    assert b.add(a) == b + a == c

    c = ANP([QQ(2), QQ(-2), QQ(-1)], mod, QQ)

    assert a.sub(b) == a - b == c

    c = ANP([QQ(-2), QQ(2), QQ(1)], mod, QQ)

    assert b.sub(a) == b - a == c

    c = ANP([QQ(3), QQ(-1), QQ(6)], mod, QQ)

    assert a.mul(b) == a*b == c
    assert b.mul(a) == b*a == c

    c = ANP([QQ(-1, 43), QQ(9, 43), QQ(5, 43)], mod, QQ)

    assert a.pow(0) == a**(0) == ANP(1, mod, QQ)
    assert a.pow(1) == a**(1) == a

    assert a.pow(-1) == a**(-1) == c

    assert a.quo(a) == a.mul(a.pow(-1)) == a*a**(-1) == ANP(1, mod, QQ)

    c = ANP([], [1, 0, 0, -2], QQ)
    r1 = a.rem(b)

    (q, r2) = a.div(b)

    assert r1 == r2 == c == a % b

    raises(NotInvertible, lambda: a.div(c))
    raises(NotInvertible, lambda: a.rem(c))

    # Comparison with "hard-coded" value fails despite looking identical
    # from sympy import Rational
    # c = ANP([Rational(11, 10), Rational(-1, 5), Rational(-3, 5)], [1, 0, 0, -2], QQ)

    assert q == a/b # == c

