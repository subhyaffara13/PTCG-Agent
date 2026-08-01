
def test_better_sqrt():
    n = Symbol('n', integer=True, nonnegative=True)
    assert sqrt(3 + 4*I) == 2 + I
    assert sqrt(3 - 4*I) == 2 - I
    assert sqrt(-3 - 4*I) == 1 - 2*I
    assert sqrt(-3 + 4*I) == 1 + 2*I
    assert sqrt(32 + 24*I) == 6 + 2*I
    assert sqrt(32 - 24*I) == 6 - 2*I
    assert sqrt(-32 - 24*I) == 2 - 6*I
    assert sqrt(-32 + 24*I) == 2 + 6*I

    # triple (3, 4, 5):
    # parity of 3 matches parity of 5 and
    # den, 4, is a square
    assert sqrt((3 + 4*I)/4) == 1 + I/2
    # triple (8, 15, 17)
    # parity of 8 doesn't match parity of 17 but
    # den/2, 8/2, is a square
    assert sqrt((8 + 15*I)/8) == (5 + 3*I)/4
    # handle the denominator
    assert sqrt((3 - 4*I)/25) == (2 - I)/5
    assert sqrt((3 - 4*I)/26) == (2 - I)/sqrt(26)
    # mul
    #  issue #12739
    assert sqrt((3 + 4*I)/(3 - 4*I)) == (3 + 4*I)/5
    assert sqrt(2/(3 + 4*I)) == sqrt(2)/5*(2 - I)
    assert sqrt(n/(3 + 4*I)).subs(n, 2) == sqrt(2)/5*(2 - I)
    assert sqrt(-2/(3 + 4*I)) == sqrt(2)/5*(1 + 2*I)
    assert sqrt(-n/(3 + 4*I)).subs(n, 2) == sqrt(2)/5*(1 + 2*I)
    # power
    assert sqrt(1/(3 + I*4)) == (2 - I)/5
    assert sqrt(1/(3 - I)) == sqrt(10)*sqrt(3 + I)/10
    # symbolic
    i = symbols('i', imaginary=True)
    assert sqrt(3/i) == Mul(sqrt(3), 1/sqrt(i), evaluate=False)
    # multiples of 1/2; don't make this too automatic
    assert sqrt(3 + 4*I)**3 == (2 + I)**3
    assert Pow(3 + 4*I, Rational(3, 2)) == 2 + 11*I
    assert Pow(6 + 8*I, Rational(3, 2)) == 2*sqrt(2)*(2 + 11*I)
    n, d = (3 + 4*I), (3 - 4*I)**3
    a = n/d
    assert a.args == (1/d, n)
    eq = sqrt(a)
    assert eq.args == (a, S.Half)
    assert expand_multinomial(eq) == sqrt((-117 + 44*I)*(3 + 4*I))/125
    assert eq.expand() == (7 - 24*I)/125

    # issue 12775
    # pos im part
    assert sqrt(2*I) == (1 + I)
    assert sqrt(2*9*I) == Mul(3, 1 + I, evaluate=False)
    assert Pow(2*I, 3*S.Half) == (1 + I)**3
    # neg im part
    assert sqrt(-I/2) == Mul(S.Half, 1 - I, evaluate=False)
    # fractional im part
    assert Pow(Rational(-9, 2)*I, Rational(3, 2)) == 27*(1 - I)**3/8

