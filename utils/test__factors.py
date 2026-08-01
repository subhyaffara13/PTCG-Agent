
def test_Factors():
    assert Factors() == Factors({}) == Factors(S.One)
    assert Factors().as_expr() is S.One
    assert Factors({x: 2, y: 3, sin(x): 4}).as_expr() == x**2*y**3*sin(x)**4
    assert Factors(S.Infinity) == Factors({oo: 1})
    assert Factors(S.NegativeInfinity) == Factors({oo: 1, -1: 1})
    # issue #18059:
    assert Factors((x**2)**S.Half).as_expr() == (x**2)**S.Half

    a = Factors({x: 5, y: 3, z: 7})
    b = Factors({      y: 4, z: 3, t: 10})

    assert a.mul(b) == a*b == Factors({x: 5, y: 7, z: 10, t: 10})

    assert a.div(b) == divmod(a, b) == \
        (Factors({x: 5, z: 4}), Factors({y: 1, t: 10}))
    assert a.quo(b) == a/b == Factors({x: 5, z: 4})
    assert a.rem(b) == a % b == Factors({y: 1, t: 10})

    assert a.pow(3) == a**3 == Factors({x: 15, y: 9, z: 21})
    assert b.pow(3) == b**3 == Factors({y: 12, z: 9, t: 30})

    assert a.gcd(b) == Factors({y: 3, z: 3})
    assert a.lcm(b) == Factors({x: 5, y: 4, z: 7, t: 10})

    a = Factors({x: 4, y: 7, t: 7})
    b = Factors({z: 1, t: 3})

    assert a.normal(b) == (Factors({x: 4, y: 7, t: 4}), Factors({z: 1}))

    assert Factors(sqrt(2)*x).as_expr() == sqrt(2)*x

    assert Factors(-I)*I == Factors()
    assert Factors({S.NegativeOne: S(3)})*Factors({S.NegativeOne: S.One, I: S(5)}) == \
        Factors(I)
    assert Factors(sqrt(I)*I) == Factors(I**(S(3)/2)) == Factors({I: S(3)/2})
    assert Factors({I: S(3)/2}).as_expr() == I**(S(3)/2)

    assert Factors(S(2)**x).div(S(3)**x) == \
        (Factors({S(2): x}), Factors({S(3): x}))
    assert Factors(2**(2*x + 2)).div(S(8)) == \
        (Factors({S(2): 2*x + 2}), Factors({S(8): S.One}))

    # coverage
    # /!\ things break if this is not True
    assert Factors({S.NegativeOne: Rational(3, 2)}) == Factors({I: S.One, S.NegativeOne: S.One})
    assert Factors({I: S.One, S.NegativeOne: Rational(1, 3)}).as_expr() == I*(-1)**Rational(1, 3)

    assert Factors(-1.) == Factors({S.NegativeOne: S.One, S(1.): 1})
    assert Factors(-2.) == Factors({S.NegativeOne: S.One, S(2.): 1})
    assert Factors((-2.)**x) == Factors({S(-2.): x})
    assert Factors(S(-2)) == Factors({S.NegativeOne: S.One, S(2): 1})
    assert Factors(S.Half) == Factors({S(2): -S.One})
    assert Factors(Rational(3, 2)) == Factors({S(3): S.One, S(2): S.NegativeOne})
    assert Factors({I: S.One}) == Factors(I)
    assert Factors({-1.0: 2, I: 1}) == Factors({S(1.0): 1, I: 1})
    assert Factors({S.NegativeOne: Rational(-3, 2)}).as_expr() == I
    A = symbols('A', commutative=False)
    assert Factors(2*A**2) == Factors({S(2): 1, A**2: 1})
    assert Factors(I) == Factors({I: S.One})
    assert Factors(x).normal(S(2)) == (Factors(x), Factors(S(2)))
    assert Factors(x).normal(S.Zero) == (Factors(), Factors(S.Zero))
    raises(ZeroDivisionError, lambda: Factors(x).div(S.Zero))
    assert Factors(x).mul(S(2)) == Factors(2*x)
    assert Factors(x).mul(S.Zero).is_zero
    assert Factors(x).mul(1/x).is_one
    assert Factors(x**sqrt(2)**3).as_expr() == x**(2*sqrt(2))
    assert Factors(x)**Factors(S(2)) == Factors(x**2)
    assert Factors(x).gcd(S.Zero) == Factors(x)
    assert Factors(x).lcm(S.Zero).is_zero
    assert Factors(S.Zero).div(x) == (Factors(S.Zero), Factors())
    assert Factors(x).div(x) == (Factors(), Factors())
    assert Factors({x: .2})/Factors({x: .2}) == Factors()
    assert Factors(x) != Factors()
    assert Factors(S.Zero).normal(x) == (Factors(S.Zero), Factors())
    n, d = x**(2 + y), x**2
    f = Factors(n)
    assert f.div(d) == f.normal(d) == (Factors(x**y), Factors())
    assert f.gcd(d) == Factors()
    d = x**y
    assert f.div(d) == f.normal(d) == (Factors(x**2), Factors())
    assert f.gcd(d) == Factors(d)
    n = d = 2**x
    f = Factors(n)
    assert f.div(d) == f.normal(d) == (Factors(), Factors())
    assert f.gcd(d) == Factors(d)
    n, d = 2**x, 2**y
    f = Factors(n)
    assert f.div(d) == f.normal(d) == (Factors({S(2): x}), Factors({S(2): y}))
    assert f.gcd(d) == Factors()

    # extraction of constant only
    n = x**(x + 3)
    assert Factors(n).normal(x**-3) == (Factors({x: x + 6}), Factors({}))
    assert Factors(n).normal(x**3) == (Factors({x: x}), Factors({}))
    assert Factors(n).normal(x**4) == (Factors({x: x}), Factors({x: 1}))
    assert Factors(n).normal(x**(y - 3)) == \
        (Factors({x: x + 6}), Factors({x: y}))
    assert Factors(n).normal(x**(y + 3)) == (Factors({x: x}), Factors({x: y}))
    assert Factors(n).normal(x**(y + 4)) == \
        (Factors({x: x}), Factors({x: y + 1}))

    assert Factors(n).div(x**-3) == (Factors({x: x + 6}), Factors({}))
    assert Factors(n).div(x**3) == (Factors({x: x}), Factors({}))
    assert Factors(n).div(x**4) == (Factors({x: x}), Factors({x: 1}))
    assert Factors(n).div(x**(y - 3)) == \
        (Factors({x: x + 6}), Factors({x: y}))
    assert Factors(n).div(x**(y + 3)) == (Factors({x: x}), Factors({x: y}))
    assert Factors(n).div(x**(y + 4)) == \
        (Factors({x: x}), Factors({x: y + 1}))

    assert Factors(3 * x / 2) == Factors({3: 1, 2: -1, x: 1})
    assert Factors(x * x / y) == Factors({x: 2, y: -1})
    assert Factors(27 * x / y**9) == Factors({27: 1, x: 1, y: -9})

