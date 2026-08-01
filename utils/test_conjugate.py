
def test_conjugate():
    M = OperationsOnlyMatrix([[0, I, 5],
                [1, 2, 0]])

    assert M.T == Matrix([[0, 1],
                          [I, 2],
                          [5, 0]])

    assert M.C == Matrix([[0, -I, 5],
                          [1,  2, 0]])
    assert M.C == M.conjugate()

    assert M.H == M.T.C
    assert M.H == Matrix([[ 0, 1],
                          [-I, 2],
                          [ 5, 0]])


def test_conjugate():
    M = Matrix([[0, I, 5],
                [1, 2, 0]])

    assert M.T == Matrix([[0, 1],
                          [I, 2],
                          [5, 0]])

    assert M.C == Matrix([[0, -I, 5],
                          [1,  2, 0]])
    assert M.C == M.conjugate()

    assert M.H == M.T.C
    assert M.H == Matrix([[ 0, 1],
                          [-I, 2],
                          [ 5, 0]])


def test_conjugate():
    M = Matrix([[0, I, 5],
                [1, 2, 0]])

    assert M.T == Matrix([[0, 1],
                          [I, 2],
                          [5, 0]])

    assert M.C == Matrix([[0, -I, 5],
                          [1,  2, 0]])
    assert M.C == M.conjugate()

    assert M.H == M.T.C
    assert M.H == Matrix([[ 0, 1],
                          [-I, 2],
                          [ 5, 0]])


def test_conjugate():
    n = Symbol('n')
    z = Symbol('z', extended_real=False)
    x = Symbol('x', extended_real=True)
    y = Symbol('y', positive=True)
    t = Symbol('t', negative=True)

    for f in [besseli, besselj, besselk, bessely, hankel1, hankel2]:
        assert f(n, -1).conjugate() != f(conjugate(n), -1)
        assert f(n, x).conjugate() != f(conjugate(n), x)
        assert f(n, t).conjugate() != f(conjugate(n), t)

    rz = randcplx(b=0.5)

    for f in [besseli, besselj, besselk, bessely]:
        assert f(n, 1 + I).conjugate() == f(conjugate(n), 1 - I)
        assert f(n, 0).conjugate() == f(conjugate(n), 0)
        assert f(n, 1).conjugate() == f(conjugate(n), 1)
        assert f(n, z).conjugate() == f(conjugate(n), conjugate(z))
        assert f(n, y).conjugate() == f(conjugate(n), y)
        assert tn(f(n, rz).conjugate(), f(conjugate(n), conjugate(rz)))

    assert hankel1(n, 1 + I).conjugate() == hankel2(conjugate(n), 1 - I)
    assert hankel1(n, 0).conjugate() == hankel2(conjugate(n), 0)
    assert hankel1(n, 1).conjugate() == hankel2(conjugate(n), 1)
    assert hankel1(n, y).conjugate() == hankel2(conjugate(n), y)
    assert hankel1(n, z).conjugate() == hankel2(conjugate(n), conjugate(z))
    assert tn(hankel1(n, rz).conjugate(), hankel2(conjugate(n), conjugate(rz)))

    assert hankel2(n, 1 + I).conjugate() == hankel1(conjugate(n), 1 - I)
    assert hankel2(n, 0).conjugate() == hankel1(conjugate(n), 0)
    assert hankel2(n, 1).conjugate() == hankel1(conjugate(n), 1)
    assert hankel2(n, y).conjugate() == hankel1(conjugate(n), y)
    assert hankel2(n, z).conjugate() == hankel1(conjugate(n), conjugate(z))
    assert tn(hankel2(n, rz).conjugate(), hankel1(conjugate(n), conjugate(rz)))


def test_conjugate():
    a = Symbol('a', real=True)
    b = Symbol('b', imaginary=True)
    assert conjugate(a) == a
    assert conjugate(I*a) == -I*a
    assert conjugate(b) == -b
    assert conjugate(I*b) == I*b
    assert conjugate(a*b) == -a*b
    assert conjugate(I*a*b) == I*a*b

    x, y = symbols('x y')
    assert conjugate(conjugate(x)) == x
    assert conjugate(x).inverse() == conjugate
    assert conjugate(x + y) == conjugate(x) + conjugate(y)
    assert conjugate(x - y) == conjugate(x) - conjugate(y)
    assert conjugate(x * y) == conjugate(x) * conjugate(y)
    assert conjugate(x / y) == conjugate(x) / conjugate(y)
    assert conjugate(-x) == -conjugate(x)

    a = Symbol('a', algebraic=True)
    t = Symbol('t', transcendental=True)
    assert re(a).is_algebraic
    assert re(x).is_algebraic is None
    assert re(t).is_algebraic is False


def test_conjugate():
    a = Symbol("a", real=True)
    b = Symbol("b", real=True)
    c = Symbol("c", imaginary=True)
    d = Symbol("d", imaginary=True)
    x = Symbol('x')
    z = a + I*b + c + I*d
    zc = a - I*b - c + I*d
    assert conjugate(z) == zc
    assert conjugate(exp(z)) == exp(zc)
    assert conjugate(exp(I*x)) == exp(-I*conjugate(x))
    assert conjugate(z**5) == zc**5
    assert conjugate(abs(x)) == abs(x)
    assert conjugate(sign(z)) == sign(zc)
    assert conjugate(sin(z)) == sin(zc)
    assert conjugate(cos(z)) == cos(zc)
    assert conjugate(tan(z)) == tan(zc)
    assert conjugate(cot(z)) == cot(zc)
    assert conjugate(sinh(z)) == sinh(zc)
    assert conjugate(cosh(z)) == cosh(zc)
    assert conjugate(tanh(z)) == tanh(zc)
    assert conjugate(coth(z)) == coth(zc)


def test_conjugate():
    assert conjugate(A).is_commutative is False
    assert (A*A).conjugate() == conjugate(A)**2
    assert (A*B).conjugate() == conjugate(A)*conjugate(B)
    assert (A*B**2).conjugate() == conjugate(A)*conjugate(B)**2
    assert (A*B - B*A).conjugate() == \
        conjugate(A)*conjugate(B) - conjugate(B)*conjugate(A)
    assert (A*B).conjugate() - (B*A).conjugate() == \
        conjugate(A)*conjugate(B) - conjugate(B)*conjugate(A)
    assert (A + I*B).conjugate() == conjugate(A) - I*conjugate(B)

