
def test_radsimp():
    r2 = sqrt(2)
    r3 = sqrt(3)
    r5 = sqrt(5)
    r7 = sqrt(7)
    assert fraction(radsimp(1/r2)) == (sqrt(2), 2)
    assert radsimp(1/(1 + r2)) == \
        -1 + sqrt(2)
    assert radsimp(1/(r2 + r3)) == \
        -sqrt(2) + sqrt(3)
    assert fraction(radsimp(1/(1 + r2 + r3))) == \
        (-sqrt(6) + sqrt(2) + 2, 4)
    assert fraction(radsimp(1/(r2 + r3 + r5))) == \
        (-sqrt(30) + 2*sqrt(3) + 3*sqrt(2), 12)
    assert fraction(radsimp(1/(1 + r2 + r3 + r5))) == (
        (-34*sqrt(10) - 26*sqrt(15) - 55*sqrt(3) - 61*sqrt(2) + 14*sqrt(30) +
        93 + 46*sqrt(6) + 53*sqrt(5), 71))
    assert fraction(radsimp(1/(r2 + r3 + r5 + r7))) == (
        (-50*sqrt(42) - 133*sqrt(5) - 34*sqrt(70) - 145*sqrt(3) + 22*sqrt(105)
        + 185*sqrt(2) + 62*sqrt(30) + 135*sqrt(7), 215))
    z = radsimp(1/(1 + r2/3 + r3/5 + r5 + r7))
    assert len((3616791619821680643598*z).args) == 16
    assert radsimp(1/z) == 1/z
    assert radsimp(1/z, max_terms=20).expand() == 1 + r2/3 + r3/5 + r5 + r7
    assert radsimp(1/(r2*3)) == \
        sqrt(2)/6
    assert radsimp(1/(r2*a + r3 + r5 + r7)) == (
        (8*sqrt(2)*a**7 - 8*sqrt(7)*a**6 - 8*sqrt(5)*a**6 - 8*sqrt(3)*a**6 -
        180*sqrt(2)*a**5 + 8*sqrt(30)*a**5 + 8*sqrt(42)*a**5 + 8*sqrt(70)*a**5
        - 24*sqrt(105)*a**4 + 84*sqrt(3)*a**4 + 100*sqrt(5)*a**4 +
        116*sqrt(7)*a**4 - 72*sqrt(70)*a**3 - 40*sqrt(42)*a**3 -
        8*sqrt(30)*a**3 + 782*sqrt(2)*a**3 - 462*sqrt(3)*a**2 -
        302*sqrt(7)*a**2 - 254*sqrt(5)*a**2 + 120*sqrt(105)*a**2 -
        795*sqrt(2)*a - 62*sqrt(30)*a + 82*sqrt(42)*a + 98*sqrt(70)*a -
        118*sqrt(105) + 59*sqrt(7) + 295*sqrt(5) + 531*sqrt(3))/(16*a**8 -
        480*a**6 + 3128*a**4 - 6360*a**2 + 3481))
    assert radsimp(1/(r2*a + r2*b + r3 + r7)) == (
        (sqrt(2)*a*(a + b)**2 - 5*sqrt(2)*a + sqrt(42)*a + sqrt(2)*b*(a +
        b)**2 - 5*sqrt(2)*b + sqrt(42)*b - sqrt(7)*(a + b)**2 - sqrt(3)*(a +
        b)**2 - 2*sqrt(3) + 2*sqrt(7))/(2*a**4 + 8*a**3*b + 12*a**2*b**2 -
        20*a**2 + 8*a*b**3 - 40*a*b + 2*b**4 - 20*b**2 + 8))
    assert radsimp(1/(r2*a + r2*b + r2*c + r2*d)) == \
        sqrt(2)/(2*a + 2*b + 2*c + 2*d)
    assert radsimp(1/(1 + r2*a + r2*b + r2*c + r2*d)) == (
        (sqrt(2)*a + sqrt(2)*b + sqrt(2)*c + sqrt(2)*d - 1)/(2*a**2 + 4*a*b +
        4*a*c + 4*a*d + 2*b**2 + 4*b*c + 4*b*d + 2*c**2 + 4*c*d + 2*d**2 - 1))
    assert radsimp((y**2 - x)/(y - sqrt(x))) == \
        sqrt(x) + y
    assert radsimp(-(y**2 - x)/(y - sqrt(x))) == \
        -(sqrt(x) + y)
    assert radsimp(1/(1 - I + a*I)) == \
        (-I*a + 1 + I)/(a**2 - 2*a + 2)
    assert radsimp(1/((-x + y)*(x - sqrt(y)))) == \
        (-x - sqrt(y))/((x - y)*(x**2 - y))
    e = (3 + 3*sqrt(2))*x*(3*x - 3*sqrt(y))
    assert radsimp(e) == x*(3 + 3*sqrt(2))*(3*x - 3*sqrt(y))
    assert radsimp(1/e) == (
        (-9*x + 9*sqrt(2)*x - 9*sqrt(y) + 9*sqrt(2)*sqrt(y))/(9*x*(9*x**2 -
        9*y)))
    assert radsimp(1 + 1/(1 + sqrt(3))) == \
        Mul(S.Half, -1 + sqrt(3), evaluate=False) + 1
    A = symbols("A", commutative=False)
    assert radsimp(x**2 + sqrt(2)*x**2 - sqrt(2)*x*A) == \
        x**2 + sqrt(2)*x**2 - sqrt(2)*x*A
    assert radsimp(1/sqrt(5 + 2 * sqrt(6))) == -sqrt(2) + sqrt(3)
    assert radsimp(1/sqrt(5 + 2 * sqrt(6))**3) == -(-sqrt(3) + sqrt(2))**3

    # issue 6532
    assert fraction(radsimp(1/sqrt(x))) == (sqrt(x), x)
    assert fraction(radsimp(1/sqrt(2*x + 3))) == (sqrt(2*x + 3), 2*x + 3)
    assert fraction(radsimp(1/sqrt(2*(x + 3)))) == (sqrt(2*x + 6), 2*x + 6)

    # issue 5994
    e = S('-(2 + 2*sqrt(2) + 4*2**(1/4))/'
        '(1 + 2**(3/4) + 3*2**(1/4) + 3*sqrt(2))')
    assert radsimp(e).expand() == -2*2**Rational(3, 4) - 2*2**Rational(1, 4) + 2 + 2*sqrt(2)

    # issue 5986 (modifications to radimp didn't initially recognize this so
    # the test is included here)
    assert radsimp(1/(-sqrt(5)/2 - S.Half + (-sqrt(5)/2 - S.Half)**2)) == 1

    # from issue 5934
    eq = (
        (-240*sqrt(2)*sqrt(sqrt(5) + 5)*sqrt(8*sqrt(5) + 40) -
        360*sqrt(2)*sqrt(-8*sqrt(5) + 40)*sqrt(-sqrt(5) + 5) -
        120*sqrt(10)*sqrt(-8*sqrt(5) + 40)*sqrt(-sqrt(5) + 5) +
        120*sqrt(2)*sqrt(-sqrt(5) + 5)*sqrt(8*sqrt(5) + 40) +
        120*sqrt(2)*sqrt(-8*sqrt(5) + 40)*sqrt(sqrt(5) + 5) +
        120*sqrt(10)*sqrt(-sqrt(5) + 5)*sqrt(8*sqrt(5) + 40) +
        120*sqrt(10)*sqrt(-8*sqrt(5) + 40)*sqrt(sqrt(5) + 5))/(-36000 -
        7200*sqrt(5) + (12*sqrt(10)*sqrt(sqrt(5) + 5) +
        24*sqrt(10)*sqrt(-sqrt(5) + 5))**2))
    assert radsimp(eq) is S.NaN  # it's 0/0

    # work with normal form
    e = 1/sqrt(sqrt(7)/7 + 2*sqrt(2) + 3*sqrt(3) + 5*sqrt(5)) + 3
    assert radsimp(e) == (
        -sqrt(sqrt(7) + 14*sqrt(2) + 21*sqrt(3) +
        35*sqrt(5))*(-11654899*sqrt(35) - 1577436*sqrt(210) - 1278438*sqrt(15)
        - 1346996*sqrt(10) + 1635060*sqrt(6) + 5709765 + 7539830*sqrt(14) +
        8291415*sqrt(21))/1300423175 + 3)

    # obey power rules
    base = sqrt(3) - sqrt(2)
    assert radsimp(1/base**3) == (sqrt(3) + sqrt(2))**3
    assert radsimp(1/(-base)**3) == -(sqrt(2) + sqrt(3))**3
    assert radsimp(1/(-base)**x) == (-base)**(-x)
    assert radsimp(1/base**x) == (sqrt(2) + sqrt(3))**x
    assert radsimp(root(1/(-1 - sqrt(2)), -x)) == (-1)**(-1/x)*(1 + sqrt(2))**(1/x)

    # recurse
    e = cos(1/(1 + sqrt(2)))
    assert radsimp(e) == cos(-sqrt(2) + 1)
    assert radsimp(e/2) == cos(-sqrt(2) + 1)/2
    assert radsimp(1/e) == 1/cos(-sqrt(2) + 1)
    assert radsimp(2/e) == 2/cos(-sqrt(2) + 1)
    assert fraction(radsimp(e/sqrt(x))) == (sqrt(x)*cos(-sqrt(2)+1), x)

    # test that symbolic denominators are not processed
    r = 1 + sqrt(2)
    assert radsimp(x/r, symbolic=False) == -x*(-sqrt(2) + 1)
    assert radsimp(x/(y + r), symbolic=False) == x/(y + 1 + sqrt(2))
    assert radsimp(x/(y + r)/r, symbolic=False) == \
        -x*(-sqrt(2) + 1)/(y + 1 + sqrt(2))

    # issue 7408
    eq = sqrt(x)/sqrt(y)
    assert radsimp(eq) == umul(sqrt(x), sqrt(y), 1/y)
    assert radsimp(eq, symbolic=False) == eq

    # issue 7498
    assert radsimp(sqrt(x)/sqrt(y)**3) == umul(sqrt(x), sqrt(y**3), 1/y**3)

    # for coverage
    eq = sqrt(x)/y**2
    assert radsimp(eq) == eq

    # handle non-Expr args
    from sympy.integrals.integrals import Integral
    eq = Integral(x/(sqrt(2) - 1), (x, 0, 1/(sqrt(2) + 1)))
    assert radsimp(eq) == Integral((sqrt(2) + 1)*x , (x, 0, sqrt(2) - 1))

    from sympy.sets import FiniteSet
    eq = FiniteSet(x/(sqrt(2) - 1))
    assert radsimp(eq) == FiniteSet((sqrt(2) + 1)*x)


def test_radsimp():
    assert radsimp(A*B - B*A) == A*B - B*A

