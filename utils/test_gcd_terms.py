
def test_gcd_terms():
    f = 2*(x + 1)*(x + 4)/(5*x**2 + 5) + (2*x + 2)*(x + 5)/(x**2 + 1)/5 + \
        (2*x + 2)*(x + 6)/(5*x**2 + 5)

    assert _gcd_terms(f) == ((Rational(6, 5))*((1 + x)/(1 + x**2)), 5 + x, 1)
    assert _gcd_terms(Add.make_args(f)) == \
        ((Rational(6, 5))*((1 + x)/(1 + x**2)), 5 + x, 1)

    newf = (Rational(6, 5))*((1 + x)*(5 + x)/(1 + x**2))
    assert gcd_terms(f) == newf
    args = Add.make_args(f)
    # non-Basic sequences of terms treated as terms of Add
    assert gcd_terms(list(args)) == newf
    assert gcd_terms(tuple(args)) == newf
    assert gcd_terms(set(args)) == newf
    # but a Basic sequence is treated as a container
    assert gcd_terms(Tuple(*args)) != newf
    assert gcd_terms(Basic(Tuple(S(1), 3*y + 3*x*y), Tuple(S(1), S(3)))) == \
        Basic(Tuple(S(1), 3*y*(x + 1)), Tuple(S(1), S(3)))
    # but we shouldn't change keys of a dictionary or some may be lost
    assert gcd_terms(Dict((x*(1 + y), S(2)), (x + x*y, y + x*y))) == \
        Dict({x*(y + 1): S(2), x + x*y: y*(1 + x)})

    assert gcd_terms((2*x + 2)**3 + (2*x + 2)**2) == 4*(x + 1)**2*(2*x + 3)

    assert gcd_terms(0) == 0
    assert gcd_terms(1) == 1
    assert gcd_terms(x) == x
    assert gcd_terms(2 + 2*x) == Mul(2, 1 + x, evaluate=False)
    arg = x*(2*x + 4*y)
    garg = 2*x*(x + 2*y)
    assert gcd_terms(arg) == garg
    assert gcd_terms(sin(arg)) == sin(garg)

    # issue 6139-like
    alpha, alpha1, alpha2, alpha3 = symbols('alpha:4')
    a = alpha**2 - alpha*x**2 + alpha + x**3 - x*(alpha + 1)
    rep = (alpha, (1 + sqrt(5))/2 + alpha1*x + alpha2*x**2 + alpha3*x**3)
    s = (a/(x - alpha)).subs(*rep).series(x, 0, 1)
    assert simplify(collect(s, x)) == -sqrt(5)/2 - Rational(3, 2) + O(x)

    # issue 5917
    assert _gcd_terms([S.Zero, S.Zero]) == (0, 0, 1)
    assert _gcd_terms([2*x + 4]) == (2, x + 2, 1)

    eq = x/(x + 1/x)
    assert gcd_terms(eq, fraction=False) == eq
    eq = x/2/y + 1/x/y
    assert gcd_terms(eq, fraction=True, clear=True) == \
        (x**2 + 2)/(2*x*y)
    assert gcd_terms(eq, fraction=True, clear=False) == \
        (x**2/2 + 1)/(x*y)
    assert gcd_terms(eq, fraction=False, clear=True) == \
        (x + 2/x)/(2*y)
    assert gcd_terms(eq, fraction=False, clear=False) == \
        (x/2 + 1/x)/y

