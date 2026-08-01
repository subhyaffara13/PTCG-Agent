
def test_Abs():
    assert str(Abs(x)) == "Abs(x)"
    assert str(Abs(Rational(1, 6))) == "1/6"
    assert str(Abs(Rational(-1, 6))) == "1/6"


def test_Abs():
    assert (Abs(interval(-0.5, 0.5)) == interval(0, 0.5)) == (True, True)
    assert (Abs(interval(-3, -2)) == interval(2, 3)) == (True, True)
    assert (Abs(-3) == interval(3, 3)) == (True, True)


def test_Abs():
    raises(TypeError, lambda: Abs(Interval(2, 3)))  # issue 8717

    x, y = symbols('x,y')
    assert sign(sign(x)) == sign(x)
    assert sign(x*y).func is sign
    assert Abs(0) == 0
    assert Abs(1) == 1
    assert Abs(-1) == 1
    assert Abs(I) == 1
    assert Abs(-I) == 1
    assert Abs(nan) is nan
    assert Abs(zoo) is oo
    assert Abs(I * pi) == pi
    assert Abs(-I * pi) == pi
    assert Abs(I * x) == Abs(x)
    assert Abs(-I * x) == Abs(x)
    assert Abs(-2*x) == 2*Abs(x)
    assert Abs(-2.0*x) == 2.0*Abs(x)
    assert Abs(2*pi*x*y) == 2*pi*Abs(x*y)
    assert Abs(conjugate(x)) == Abs(x)
    assert conjugate(Abs(x)) == Abs(x)
    assert Abs(x).expand(complex=True) == sqrt(re(x)**2 + im(x)**2)

    a = Symbol('a', positive=True)
    assert Abs(2*pi*x*a) == 2*pi*a*Abs(x)
    assert Abs(2*pi*I*x*a) == 2*pi*a*Abs(x)

    x = Symbol('x', real=True)
    n = Symbol('n', integer=True)
    assert Abs((-1)**n) == 1
    assert x**(2*n) == Abs(x)**(2*n)
    assert Abs(x).diff(x) == sign(x)
    assert abs(x) == Abs(x)  # Python built-in
    assert Abs(x)**3 == x**2*Abs(x)
    assert Abs(x)**4 == x**4
    assert (
        Abs(x)**(3*n)).args == (Abs(x), 3*n)  # leave symbolic odd unchanged
    assert (1/Abs(x)).args == (Abs(x), -1)
    assert 1/Abs(x)**3 == 1/(x**2*Abs(x))
    assert Abs(x)**-3 == Abs(x)/(x**4)
    assert Abs(x**3) == x**2*Abs(x)
    assert Abs(I**I) == exp(-pi/2)
    assert Abs((4 + 5*I)**(6 + 7*I)) == 68921*exp(-7*atan(Rational(5, 4)))
    y = Symbol('y', real=True)
    assert Abs(I**y) == 1
    y = Symbol('y')
    assert Abs(I**y) == exp(-pi*im(y)/2)

    x = Symbol('x', imaginary=True)
    assert Abs(x).diff(x) == -sign(x)

    eq = -sqrt(10 + 6*sqrt(3)) + sqrt(1 + sqrt(3)) + sqrt(3 + 3*sqrt(3))
    # if there is a fast way to know when you can and when you cannot prove an
    # expression like this is zero then the equality to zero is ok
    assert abs(eq).func is Abs or abs(eq) == 0
    # but sometimes it's hard to do this so it's better not to load
    # abs down with tests that will be very slow
    q = 1 + sqrt(2) - 2*sqrt(3) + 1331*sqrt(6)
    p = expand(q**3)**Rational(1, 3)
    d = p - q
    assert abs(d).func is Abs or abs(d) == 0

    assert Abs(4*exp(pi*I/4)) == 4
    assert Abs(3**(2 + I)) == 9
    assert Abs((-3)**(1 - I)) == 3*exp(pi)

    assert Abs(oo) is oo
    assert Abs(-oo) is oo
    assert Abs(oo + I) is oo
    assert Abs(oo + I*oo) is oo

    a = Symbol('a', algebraic=True)
    t = Symbol('t', transcendental=True)
    x = Symbol('x')
    assert re(a).is_algebraic
    assert re(x).is_algebraic is None
    assert re(t).is_algebraic is False
    assert Abs(x).fdiff() == sign(x)
    raises(ArgumentIndexError, lambda: Abs(x).fdiff(2))

    # doesn't have recursion error
    arg = sqrt(acos(1 - I)*acos(1 + I))
    assert abs(arg) == arg

    # special handling to put Abs in denom
    assert abs(1/x) == 1/Abs(x)
    e = abs(2/x**2)
    assert e.is_Mul and e == 2/Abs(x**2)
    assert unchanged(Abs, y/x)
    assert unchanged(Abs, x/(x + 1))
    assert unchanged(Abs, x*y)
    p = Symbol('p', positive=True)
    assert abs(x/p) == abs(x)/p

    # coverage
    assert unchanged(Abs, Symbol('x', real=True)**y)
    # issue 19627
    f = Function('f', positive=True)
    assert sqrt(f(x)**2) == f(x)
    # issue 21625
    assert unchanged(Abs, S("im(acos(-i + acosh(-g + i)))"))


def test_Abs():
    assert refine(Abs(x), Q.positive(x)) == x
    assert refine(1 + Abs(x), Q.positive(x)) == 1 + x
    assert refine(Abs(x), Q.negative(x)) == -x
    assert refine(1 + Abs(x), Q.negative(x)) == 1 - x

    assert refine(Abs(x**2)) != x**2
    assert refine(Abs(x**2), Q.real(x)) == x**2

