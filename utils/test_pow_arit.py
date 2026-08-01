
def test_pow_arit():
    n1 = Rational(1)
    n2 = Rational(2)
    n5 = Rational(5)
    e = a*a
    assert e == a**2
    e = a*a*a
    assert e == a**3
    e = a*a*a*a**Rational(6)
    assert e == a**9
    e = a*a*a*a**Rational(6) - a**Rational(9)
    assert e == Rational(0)
    e = a**(b - b)
    assert e == Rational(1)
    e = (a + Rational(1) - a)**b
    assert e == Rational(1)

    e = (a + b + c)**n2
    assert e == (a + b + c)**2
    assert e.expand() == 2*b*c + 2*a*c + 2*a*b + a**2 + c**2 + b**2

    e = (a + b)**n2
    assert e == (a + b)**2
    assert e.expand() == 2*a*b + a**2 + b**2

    e = (a + b)**(n1/n2)
    assert e == sqrt(a + b)
    assert e.expand() == sqrt(a + b)

    n = n5**(n1/n2)
    assert n == sqrt(5)
    e = n*a*b - n*b*a
    assert e == Rational(0)
    e = n*a*b + n*b*a
    assert e == 2*a*b*sqrt(5)
    assert e.diff(a) == 2*b*sqrt(5)
    assert e.diff(a) == 2*b*sqrt(5)
    e = a/b**2
    assert e == a*b**(-2)

    assert sqrt(2*(1 + sqrt(2))) == (2*(1 + 2**S.Half))**S.Half

    x = Symbol('x')
    y = Symbol('y')

    assert ((x*y)**3).expand() == y**3 * x**3
    assert ((x*y)**-3).expand() == y**-3 * x**-3

    assert (x**5*(3*x)**(3)).expand() == 27 * x**8
    assert (x**5*(-3*x)**(3)).expand() == -27 * x**8
    assert (x**5*(3*x)**(-3)).expand() == x**2 * Rational(1, 27)
    assert (x**5*(-3*x)**(-3)).expand() == x**2 * Rational(-1, 27)

    # expand_power_exp
    _x = Symbol('x', zero=False)
    _y = Symbol('y', zero=False)
    assert (_x**(y**(x + exp(x + y)) + z)).expand(deep=False) == \
        _x**z*_x**(y**(x + exp(x + y)))
    assert (_x**(_y**(x + exp(x + y)) + z)).expand() == \
        _x**z*_x**(_y**x*_y**(exp(x)*exp(y)))

    n = Symbol('n', even=False)
    k = Symbol('k', even=True)
    o = Symbol('o', odd=True)

    assert unchanged(Pow, -1, x)
    assert unchanged(Pow, -1, n)
    assert (-2)**k == 2**k
    assert (-1)**k == 1
    assert (-1)**o == -1

