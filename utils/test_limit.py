
def test_limit():
    x, y = symbols('x y')
    m = CalculusOnlyMatrix(2, 1, [1/x, y])
    assert m.limit(x, 5) == Matrix(2, 1, [Rational(1, 5), y])


def test_limit():
    A = Matrix(((1, 4, sin(x)/x), (y, 2, 4), (10, 5, x**2 + 1)))
    assert A.limit(x, 0) == Matrix(((1, 4, 1), (y, 2, 4), (10, 5, 1)))


def test_limit():
    x, y = symbols('x y')
    m = Matrix(2, 1, [1/x, y])
    assert m.limit(x, 5) == Matrix(2, 1, [Rational(1, 5), y])
    A = Matrix(((1, 4, sin(x)/x), (y, 2, 4), (10, 5, x**2 + 1)))
    assert A.limit(x, 0) == Matrix(((1, 4, 1), (y, 2, 4), (10, 5, 1)))

