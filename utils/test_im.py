
def test_im():
    x, y = symbols('x,y')
    a, b = symbols('a,b', real=True)

    r = Symbol('r', real=True)
    i = Symbol('i', imaginary=True)

    assert im(nan) is nan

    assert im(oo*I) is oo
    assert im(-oo*I) is -oo

    assert im(0) == 0

    assert im(1) == 0
    assert im(-1) == 0

    assert im(E*I) == E
    assert im(-E*I) == -E

    assert unchanged(im, x)
    assert im(x*I) == re(x)
    assert im(r*I) == r
    assert im(r) == 0
    assert im(i*I) == 0
    assert im(i) == -I * i

    assert im(x + y) == im(x) + im(y)
    assert im(x + r) == im(x)
    assert im(x + r*I) == im(x) + r

    assert im(im(x)*I) == im(x)

    assert im(2 + I) == 1
    assert im(x + I) == im(x) + 1

    assert im(x + y*I) == im(x) + re(y)
    assert im(x + r*I) == im(x) + r

    assert im(log(2*I)) == pi/2

    assert im((2 + I)**2).expand(complex=True) == 4

    assert im(conjugate(x)) == -im(x)
    assert conjugate(im(x)) == im(x)

    assert im(x).as_real_imag() == (im(x), 0)

    assert im(i*r*x).diff(r) == im(i*x)
    assert im(i*r*x).diff(i) == -I * re(r*x)

    assert im(
        sqrt(a + b*I)) == (a**2 + b**2)**Rational(1, 4)*sin(atan2(b, a)/2)
    assert im(a * (2 + b*I)) == a*b

    assert im((1 + sqrt(a + b*I))/2) == \
        (a**2 + b**2)**Rational(1, 4)*sin(atan2(b, a)/2)/2

    assert im(x).rewrite(re) == -S.ImaginaryUnit * (x - re(x))
    assert (x + im(y)).rewrite(im, re) == x - S.ImaginaryUnit * (y - re(y))

    a = Symbol('a', algebraic=True)
    t = Symbol('t', transcendental=True)
    x = Symbol('x')
    assert re(a).is_algebraic
    assert re(x).is_algebraic is None
    assert re(t).is_algebraic is False

    assert im(S.ComplexInfinity) is S.NaN

    n, m, l = symbols('n m l')
    A = MatrixSymbol('A',n,m)

    assert im(A) == (S.One/(2*I)) * (A - conjugate(A))

    A = Matrix([[1 + 4*I, 2],[0, -3*I]])
    assert im(A) == Matrix([[4, 0],[0, -3]])

    A = ImmutableMatrix([[1 + 3*I, 3-2*I],[0, 2*I]])
    assert im(A) == ImmutableMatrix([[3, -2],[0, 2]])

    X = ImmutableSparseMatrix(
            [[i*I + i for i in range(5)] for i in range(5)])
    Y = SparseMatrix([list(range(5)) for i in range(5)])
    assert im(X).as_immutable() == Y

    X = FunctionMatrix(3, 3, Lambda((n, m), n + m*I))
    assert im(X) == Matrix([[0, 1, 2], [0, 1, 2], [0, 1, 2]])


def test_im():
    assert refine(im(x), Q.imaginary(x)) == -I*x
    assert refine(im(x), Q.real(x)) is S.Zero
    assert refine(im(x+y), Q.imaginary(x) & Q.imaginary(y)) == -I*x - I*y
    assert refine(im(x+y), Q.real(x) & Q.imaginary(y)) == -I*y
    assert refine(im(x*y), Q.imaginary(x) & Q.real(y)) == -I*x*y
    assert refine(im(x*y), Q.imaginary(x) & Q.imaginary(y)) == 0
    assert refine(im(1/x), Q.imaginary(x)) == -I/x
    assert refine(im(x*y*z), Q.imaginary(x) & Q.imaginary(y)
        & Q.imaginary(z)) == -I*x*y*z

