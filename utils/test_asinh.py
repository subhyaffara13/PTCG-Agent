
def test_asinh():
    R, x, y = ring('x, y', QQ)
    assert rs_asinh(x, x, 9) == -5/112*x**7 + 3/40*x**5 - 1/6*x**3 + x
    assert rs_asinh(x*y + x**2*y**3, x, 9) == 3/4*x**8*y**11 - 5/16*x**8*y**9 + \
        3/4*x**7*y**9 - 5/112*x**7*y**7 - 1/6*x**6*y**9 + 3/8*x**6*y**7 - 1/2*x \
        **5*y**7 + 3/40*x**5*y**5 - 1/2*x**4*y**5 - 1/6*x**3*y**3 + x**2*y**3 + x*y

    # Constant term in series
    a = symbols('a')
    R, x, y = ring('x, y', EX)
    assert rs_asinh(x + a, x, 3) == -EX(a/(2*a**2*sqrt(a**2 + 1) + 2*sqrt(a**2 + 1))) \
        *x**2 + EX(1/sqrt(a**2 + 1))*x + EX(asinh(a))
    assert rs_asinh(x + x**2*y + a, x, 3) == EX(1/sqrt(a**2 + 1))*x**2*y - EX(a/(2*a**2 \
        *sqrt(a**2 + 1) + 2*sqrt(a**2 + 1)))*x**2 + EX(1/sqrt(a**2 + 1))*x + EX(asinh(a))

    p = x + x ** 2 + 5
    assert rs_asinh(p, x, 10).compose(x, 10) == EX(asinh(5) + 4643789843094995*sqrt(26)/\
        205564141692)


def test_asinh():
    a = asinh(interval(1, 2))
    assert a.start == np.arcsinh(1)
    assert a.end == np.arcsinh(2)

    a = asinh(0.5)
    assert a.start == np.arcsinh(0.5)
    assert a.end == np.arcsinh(0.5)


def test_asinh():
    x, y = symbols('x,y')
    assert unchanged(asinh, x)
    assert asinh(-x) == -asinh(x)

    # at specific points
    assert asinh(nan) is nan
    assert asinh( 0) == 0
    assert asinh(+1) == log(sqrt(2) + 1)

    assert asinh(-1) == log(sqrt(2) - 1)
    assert asinh(I) == pi*I/2
    assert asinh(-I) == -pi*I/2
    assert asinh(I/2) == pi*I/6
    assert asinh(-I/2) == -pi*I/6

    # at infinites
    assert asinh(oo) is oo
    assert asinh(-oo) is -oo

    assert asinh(I*oo) is oo
    assert asinh(-I *oo) is -oo

    assert asinh(zoo) is zoo

    # properties
    assert asinh(I *(sqrt(3) - 1)/(2**Rational(3, 2))) == pi*I/12
    assert asinh(-I *(sqrt(3) - 1)/(2**Rational(3, 2))) == -pi*I/12

    assert asinh(I*(sqrt(5) - 1)/4) == pi*I/10
    assert asinh(-I*(sqrt(5) - 1)/4) == -pi*I/10

    assert asinh(I*(sqrt(5) + 1)/4) == pi*I*Rational(3, 10)
    assert asinh(-I*(sqrt(5) + 1)/4) == pi*I*Rational(-3, 10)

    # reality
    assert asinh(S(2)).is_real is True
    assert asinh(S(2)).is_finite is True
    assert asinh(S(-2)).is_real is True
    assert asinh(S(oo)).is_extended_real is True
    assert asinh(-S(oo)).is_real is False
    assert (asinh(2) - oo) == -oo
    assert asinh(symbols('y', real=True)).is_real is True

    # Symmetry
    assert asinh(Rational(-1, 2)) == -asinh(S.Half)

    # inverse composition
    assert unchanged(asinh, sinh(Symbol('v1')))

    assert asinh(sinh(0, evaluate=False)) == 0
    assert asinh(sinh(-3, evaluate=False)) == -3
    assert asinh(sinh(2, evaluate=False)) == 2
    assert asinh(sinh(I, evaluate=False)) == I
    assert asinh(sinh(-I, evaluate=False)) == -I
    assert asinh(sinh(5*I, evaluate=False)) == -2*I*pi + 5*I
    assert asinh(sinh(15 + 11*I)) == 15 - 4*I*pi + 11*I
    assert asinh(sinh(-73 + 97*I)) == 73 - 97*I + 31*I*pi
    assert asinh(sinh(-7 - 23*I)) == 7 - 7*I*pi + 23*I
    assert asinh(sinh(13 - 3*I)) == -13 - I*pi + 3*I
    p = Symbol('p', positive=True)
    assert asinh(p).is_zero is False
    assert asinh(sinh(0, evaluate=False), evaluate=False).is_zero is True

