
def test_as_real_imag():
    m1 = OperationsOnlyMatrix(2, 2, [1, 2, 3, 4])
    m3 = OperationsOnlyMatrix(2, 2,
        [1 + S.ImaginaryUnit, 2 + 2*S.ImaginaryUnit,
        3 + 3*S.ImaginaryUnit, 4 + 4*S.ImaginaryUnit])

    a, b = m3.as_real_imag()
    assert a == m1
    assert b == m1


def test_as_real_imag():
    m1 = Matrix(2,2,[1,2,3,4])
    m2 = m1*S.ImaginaryUnit
    m3 = m1 + m2

    for kls in classes:
        a,b = kls(m3).as_real_imag()
        assert list(a) == list(m1)
        assert list(b) == list(m1)


def test_as_real_imag():
    m1 = Matrix(2,2,[1,2,3,4])
    m2 = m1*S.ImaginaryUnit
    m3 = m1 + m2

    for kls in all_classes:
        a,b = kls(m3).as_real_imag()
        assert list(a) == list(m1)
        assert list(b) == list(m1)


def test_as_real_imag():
    n = pi**1000
    # the special code for working out the real
    # and complex parts of a power with Integer exponent
    # should not run if there is no imaginary part, hence
    # this should not hang
    assert n.as_real_imag() == (n, 0)

    # issue 6261
    x = Symbol('x')
    assert sqrt(x).as_real_imag() == \
        ((re(x)**2 + im(x)**2)**Rational(1, 4)*cos(atan2(im(x), re(x))/2),
     (re(x)**2 + im(x)**2)**Rational(1, 4)*sin(atan2(im(x), re(x))/2))

    # issue 3853
    a, b = symbols('a,b', real=True)
    assert ((1 + sqrt(a + b*I))/2).as_real_imag() == \
           (
               (a**2 + b**2)**Rational(
                   1, 4)*cos(atan2(b, a)/2)/2 + S.Half,
               (a**2 + b**2)**Rational(1, 4)*sin(atan2(b, a)/2)/2)

    assert sqrt(a**2).as_real_imag() == (sqrt(a**2), 0)
    i = symbols('i', imaginary=True)
    assert sqrt(i**2).as_real_imag() == (0, abs(i))

    assert ((1 + I)/(1 - I)).as_real_imag() == (0, 1)
    assert ((1 + I)**3/(1 - I)).as_real_imag() == (-2, 0)


def test_as_real_imag():
    # This is for https://github.com/sympy/sympy/issues/17142
    # If it start failing again in irrelevant builds or in the master
    # please open up the issue again.
    expr = atan(I/(I + I*tan(1)))
    assert expr.as_real_imag() == (expr, 0)

