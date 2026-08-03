import re

def test_re():
    x, y = symbols('x,y')
    a, b = symbols('a,b', real=True)

    r = Symbol('r', real=True)
    i = Symbol('i', imaginary=True)

    assert re(nan) is nan

    assert re(oo) is oo
    assert re(-oo) is -oo

    assert re(0) == 0

    assert re(1) == 1
    assert re(-1) == -1

    assert re(E) == E
    assert re(-E) == -E

    assert unchanged(re, x)
    assert re(x*I) == -im(x)
    assert re(r*I) == 0
    assert re(r) == r
    assert re(i*I) == I * i
    assert re(i) == 0

    assert re(x + y) == re(x) + re(y)
    assert re(x + r) == re(x) + r

    assert re(re(x)) == re(x)

    assert re(2 + I) == 2
    assert re(x + I) == re(x)

    assert re(x + y*I) == re(x) - im(y)
    assert re(x + r*I) == re(x)

    assert re(log(2*I)) == log(2)

    assert re((2 + I)**2).expand(complex=True) == 3

    assert re(conjugate(x)) == re(x)
    assert conjugate(re(x)) == re(x)

    assert re(x).as_real_imag() == (re(x), 0)

    assert re(i*r*x).diff(r) == re(i*x)
    assert re(i*r*x).diff(i) == I*r*im(x)

    assert re(
        sqrt(a + b*I)) == (a**2 + b**2)**Rational(1, 4)*cos(atan2(b, a)/2)
    assert re(a * (2 + b*I)) == 2*a

    assert re((1 + sqrt(a + b*I))/2) == \
        (a**2 + b**2)**Rational(1, 4)*cos(atan2(b, a)/2)/2 + S.Half

    assert re(x).rewrite(im) == x - S.ImaginaryUnit*im(x)
    assert (x + re(y)).rewrite(re, im) == x + y - S.ImaginaryUnit*im(y)

    a = Symbol('a', algebraic=True)
    t = Symbol('t', transcendental=True)
    x = Symbol('x')
    assert re(a).is_algebraic
    assert re(x).is_algebraic is None
    assert re(t).is_algebraic is False

    assert re(S.ComplexInfinity) is S.NaN

    n, m, l = symbols('n m l')
    A = MatrixSymbol('A',n,m)
    assert re(A) == (S.Half) * (A + conjugate(A))

    A = Matrix([[1 + 4*I,2],[0, -3*I]])
    assert re(A) == Matrix([[1, 2],[0, 0]])

    A = ImmutableMatrix([[1 + 3*I, 3-2*I],[0, 2*I]])
    assert re(A) == ImmutableMatrix([[1, 3],[0, 0]])

    X = SparseMatrix([[2*j + i*I for i in range(5)] for j in range(5)])
    assert re(X) - Matrix([[0, 0, 0, 0, 0],
                           [2, 2, 2, 2, 2],
                           [4, 4, 4, 4, 4],
                           [6, 6, 6, 6, 6],
                           [8, 8, 8, 8, 8]]) == Matrix.zeros(5)

    assert im(X) - Matrix([[0, 1, 2, 3, 4],
                           [0, 1, 2, 3, 4],
                           [0, 1, 2, 3, 4],
                           [0, 1, 2, 3, 4],
                           [0, 1, 2, 3, 4]]) == Matrix.zeros(5)

    X = FunctionMatrix(3, 3, Lambda((n, m), n + m*I))
    assert re(X) == Matrix([[0, 0, 0], [1, 1, 1], [2, 2, 2]])


def test_re():
    assert refine(re(x), Q.real(x)) == x
    assert refine(re(x), Q.imaginary(x)) is S.Zero
    assert refine(re(x+y), Q.real(x) & Q.real(y)) == x + y
    assert refine(re(x+y), Q.real(x) & Q.imaginary(y)) == x
    assert refine(re(x*y), Q.real(x) & Q.real(y)) == x * y
    assert refine(re(x*y), Q.real(x) & Q.imaginary(y)) == 0
    assert refine(re(x*y*z), Q.real(x) & Q.real(y) & Q.real(z)) == x * y * z

