
def test_expand():
    m0 = OperationsOnlyMatrix([[x*(x + y), 2], [((x + y)*y)*x, x*(y + x*(x + y))]])
    # Test if expand() returns a matrix
    m1 = m0.expand()
    assert m1 == Matrix(
        [[x*y + x**2, 2], [x*y**2 + y*x**2, x*y + y*x**2 + x**3]])

    a = Symbol('a', real=True)

    assert OperationsOnlyMatrix(1, 1, [exp(I*a)]).expand(complex=True) == \
           Matrix([cos(a) + I*sin(a)])


def test_expand():
    m0 = Matrix([[x*(x + y), 2], [((x + y)*y)*x, x*(y + x*(x + y))]])
    # Test if expand() returns a matrix
    m1 = m0.expand()
    assert m1 == Matrix(
        [[x*y + x**2, 2], [x*y**2 + y*x**2, x*y + y*x**2 + x**3]])

    a = Symbol('a', real=True)

    assert Matrix([exp(I*a)]).expand(complex=True) == \
        Matrix([cos(a) + I*sin(a)])

    assert Matrix([[0, 1, 2], [0, 0, -1], [0, 0, 0]]).exp() == Matrix([
        [1, 1, Rational(3, 2)],
        [0, 1, -1],
        [0, 0, 1]]
    )


def test_expand():
    m0 = Matrix([[x*(x + y), 2], [((x + y)*y)*x, x*(y + x*(x + y))]])
    # Test if expand() returns a matrix
    m1 = m0.expand()
    assert m1 == Matrix(
        [[x*y + x**2, 2], [x*y**2 + y*x**2, x*y + y*x**2 + x**3]])

    a = Symbol('a', real=True)

    assert Matrix([exp(I*a)]).expand(complex=True) == \
        Matrix([cos(a) + I*sin(a)])

    assert Matrix([[0, 1, 2], [0, 0, -1], [0, 0, 0]]).exp() == Matrix([
        [1, 1, Rational(3, 2)],
        [0, 1, -1],
        [0, 0, 1]]
    )


def test_expand():
    e = Integral(f(x)+f(x**2), (x, 1, y))
    assert e.expand() == Integral(f(x), (x, 1, y)) + Integral(f(x**2), (x, 1, y))
    e = Integral(f(x)+f(x**2), (x, 1, oo))
    assert e.expand() == e
    assert e.expand(force=True) == Integral(f(x), (x, 1, oo)) + \
           Integral(f(x**2), (x, 1, oo))


def test_expand():
    assert expand_func(besselj(S.Half, z).rewrite(jn)) == \
        sqrt(2)*sin(z)/(sqrt(pi)*sqrt(z))
    assert expand_func(bessely(S.Half, z).rewrite(yn)) == \
        -sqrt(2)*cos(z)/(sqrt(pi)*sqrt(z))

    # XXX: teach sin/cos to work around arguments like
    # x*exp_polar(I*pi*n/2).  Then change besselsimp -> expand_func
    assert besselsimp(besselj(S.Half, z)) == sqrt(2)*sin(z)/(sqrt(pi)*sqrt(z))
    assert besselsimp(besselj(Rational(-1, 2), z)) == sqrt(2)*cos(z)/(sqrt(pi)*sqrt(z))
    assert besselsimp(besselj(Rational(5, 2), z)) == \
        -sqrt(2)*(z**2*sin(z) + 3*z*cos(z) - 3*sin(z))/(sqrt(pi)*z**Rational(5, 2))
    assert besselsimp(besselj(Rational(-5, 2), z)) == \
        -sqrt(2)*(z**2*cos(z) - 3*z*sin(z) - 3*cos(z))/(sqrt(pi)*z**Rational(5, 2))

    assert besselsimp(bessely(S.Half, z)) == \
        -(sqrt(2)*cos(z))/(sqrt(pi)*sqrt(z))
    assert besselsimp(bessely(Rational(-1, 2), z)) == sqrt(2)*sin(z)/(sqrt(pi)*sqrt(z))
    assert besselsimp(bessely(Rational(5, 2), z)) == \
        sqrt(2)*(z**2*cos(z) - 3*z*sin(z) - 3*cos(z))/(sqrt(pi)*z**Rational(5, 2))
    assert besselsimp(bessely(Rational(-5, 2), z)) == \
        -sqrt(2)*(z**2*sin(z) + 3*z*cos(z) - 3*sin(z))/(sqrt(pi)*z**Rational(5, 2))

    assert besselsimp(besseli(S.Half, z)) == sqrt(2)*sinh(z)/(sqrt(pi)*sqrt(z))
    assert besselsimp(besseli(Rational(-1, 2), z)) == \
        sqrt(2)*cosh(z)/(sqrt(pi)*sqrt(z))
    assert besselsimp(besseli(Rational(5, 2), z)) == \
        sqrt(2)*(z**2*sinh(z) - 3*z*cosh(z) + 3*sinh(z))/(sqrt(pi)*z**Rational(5, 2))
    assert besselsimp(besseli(Rational(-5, 2), z)) == \
        sqrt(2)*(z**2*cosh(z) - 3*z*sinh(z) + 3*cosh(z))/(sqrt(pi)*z**Rational(5, 2))

    assert besselsimp(besselk(S.Half, z)) == \
        besselsimp(besselk(Rational(-1, 2), z)) == sqrt(pi)*exp(-z)/(sqrt(2)*sqrt(z))
    assert besselsimp(besselk(Rational(5, 2), z)) == \
        besselsimp(besselk(Rational(-5, 2), z)) == \
        sqrt(2)*sqrt(pi)*(z**2 + 3*z + 3)*exp(-z)/(2*z**Rational(5, 2))

    n = Symbol('n', integer=True, positive=True)

    assert expand_func(besseli(n + 2, z)) == \
        besseli(n, z) + (-2*n - 2)*(-2*n*besseli(n, z)/z + besseli(n - 1, z))/z
    assert expand_func(besselj(n + 2, z)) == \
        -besselj(n, z) + (2*n + 2)*(2*n*besselj(n, z)/z - besselj(n - 1, z))/z
    assert expand_func(besselk(n + 2, z)) == \
        besselk(n, z) + (2*n + 2)*(2*n*besselk(n, z)/z + besselk(n - 1, z))/z
    assert expand_func(bessely(n + 2, z)) == \
        -bessely(n, z) + (2*n + 2)*(2*n*bessely(n, z)/z - bessely(n - 1, z))/z

    assert expand_func(besseli(n + S.Half, z).rewrite(jn)) == \
        (sqrt(2)*sqrt(z)*exp(-I*pi*(n + S.Half)/2) *
         exp_polar(I*pi/4)*jn(n, z*exp_polar(I*pi/2))/sqrt(pi))
    assert expand_func(besselj(n + S.Half, z).rewrite(jn)) == \
        sqrt(2)*sqrt(z)*jn(n, z)/sqrt(pi)

    r = Symbol('r', real=True)
    p = Symbol('p', positive=True)
    i = Symbol('i', integer=True)

    for besselx in [besselj, bessely, besseli, besselk]:
        assert besselx(i, p).is_extended_real is True
        assert besselx(i, x).is_extended_real is None
        assert besselx(x, z).is_extended_real is None

    for besselx in [besselj, besseli]:
        assert besselx(i, r).is_extended_real is True
    for besselx in [bessely, besselk]:
        assert besselx(i, r).is_extended_real is None

    for besselx in [besselj, bessely, besseli, besselk]:
        assert expand_func(besselx(oo, x)) == besselx(oo, x, evaluate=False)
        assert expand_func(besselx(-oo, x)) == besselx(-oo, x, evaluate=False)


def test_expand():
    f = (16 - 2*sqrt(29))**2
    assert f.expand() == 372 - 64*sqrt(29)
    f = (Integer(1)/2 + I/2)**10
    assert f.expand() == I/32
    f = (Integer(1)/2 + I)**10
    assert f.expand() == Integer(237)/1024 - 779*I/256


def test_expand():
    assert expand((A*B)**2) == A*B*A*B
    assert expand(A*B - B*A) == A*B - B*A
    assert expand((A*B/A)**2) == A*B*B/A
    assert expand(B*A*(A + B)*B) == B*A**2*B + B*A*B**2
    assert expand(B*A*(A + C)*B) == B*A**2*B + B*A*C*B


def test_expand():
    assert (2**(-1 - x)).expand() == S.Half*2**(-x)

