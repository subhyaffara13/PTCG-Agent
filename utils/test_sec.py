
def test_sec():
    x = symbols('x', real=True)
    z = symbols('z')

    assert sec.nargs == FiniteSet(1)

    assert sec(zoo) is nan
    assert sec(0) == 1
    assert sec(pi) == -1
    assert sec(pi/2) is zoo
    assert sec(-pi/2) is zoo
    assert sec(pi/6) == 2*sqrt(3)/3
    assert sec(pi/3) == 2
    assert sec(pi*Rational(5, 2)) is zoo
    assert sec(pi*Rational(9, 7)) == -sec(pi*Rational(2, 7))
    assert sec(pi*Rational(3, 4)) == -sqrt(2)  # issue 8421
    assert sec(I) == 1/cosh(1)
    assert sec(x*I) == 1/cosh(x)
    assert sec(-x) == sec(x)

    assert sec(asec(x)) == x

    assert sec(z).conjugate() == sec(conjugate(z))

    assert (sec(z).as_real_imag() ==
    (cos(re(z))*cosh(im(z))/(sin(re(z))**2*sinh(im(z))**2 +
                             cos(re(z))**2*cosh(im(z))**2),
     sin(re(z))*sinh(im(z))/(sin(re(z))**2*sinh(im(z))**2 +
                             cos(re(z))**2*cosh(im(z))**2)))

    assert sec(x).expand(trig=True) == 1/cos(x)
    assert sec(2*x).expand(trig=True) == 1/(2*cos(x)**2 - 1)

    assert sec(x).is_extended_real == True
    assert sec(z).is_real == None

    assert sec(a).is_algebraic is None
    assert sec(na).is_algebraic is False

    assert sec(x).as_leading_term() == sec(x)

    assert sec(0, evaluate=False).is_finite == True
    assert sec(x).is_finite == None
    assert sec(pi/2, evaluate=False).is_finite == False

    assert series(sec(x), x, x0=0, n=6) == 1 + x**2/2 + 5*x**4/24 + O(x**6)

    # https://github.com/sympy/sympy/issues/7166
    assert series(sqrt(sec(x))) == 1 + x**2/4 + 7*x**4/96 + O(x**6)

    # https://github.com/sympy/sympy/issues/7167
    assert (series(sqrt(sec(x)), x, x0=pi*3/2, n=4) ==
            1/sqrt(x - pi*Rational(3, 2)) + (x - pi*Rational(3, 2))**Rational(3, 2)/12 +
            (x - pi*Rational(3, 2))**Rational(7, 2)/160 + O((x - pi*Rational(3, 2))**4, (x, pi*Rational(3, 2))))

    assert sec(x).diff(x) == tan(x)*sec(x)

    # Taylor Term checks
    assert sec(z).taylor_term(4, z) == 5*z**4/24
    assert sec(z).taylor_term(6, z) == 61*z**6/720
    assert sec(z).taylor_term(5, z) == 0

