
def test_abs():
    a = Symbol('a')
    assert abs(x).nseries(x, n=4) == x
    assert abs(-x).nseries(x, n=4) == x
    assert abs(x + 1).nseries(x, n=4) == x + 1
    assert abs(sin(x)).nseries(x, n=4) == x - Rational(1, 6)*x**3 + O(x**4)
    assert abs(sin(-x)).nseries(x, n=4) == x - Rational(1, 6)*x**3 + O(x**4)
    assert abs(x - a).nseries(x, 1) == -a*sign(1 - a) + (x - 1)*sign(1 - a) + sign(1 - a)


def test_abs():
    m = ArithmeticOnlyMatrix([[1, -2], [x, y]])
    assert abs(m) == ArithmeticOnlyMatrix([[1, 2], [Abs(x), Abs(y)]])


def test_abs():
    m = Matrix(1, 2, [-3, x])
    n = Matrix(1, 2, [3, Abs(x)])
    assert abs(m) == n


def test_abs():
    m = Matrix([[1, -2], [x, y]])
    assert abs(m) == Matrix([[1, 2], [Abs(x), Abs(y)]])
    m = Matrix(1, 2, [-3, x])
    n = Matrix(1, 2, [3, Abs(x)])
    assert abs(m) == n


def test_abs():
    # this tests that abs calls Abs; don't rename to
    # test_Abs since that test is already above
    a = Symbol('a', positive=True)
    assert abs(I*(1 + a)**2) == (1 + a)**2


def test_abs():
    assert satask(Q.nonnegative(abs(x))) is True
    assert satask(Q.positive(abs(x)), ~Q.zero(x)) is True
    assert satask(Q.zero(x), ~Q.zero(abs(x))) is False
    assert satask(Q.zero(x), Q.zero(abs(x))) is True
    assert satask(Q.nonzero(x), ~Q.zero(abs(x))) is None # x could be complex
    assert satask(Q.zero(abs(x)), Q.zero(x)) is True

