
def test_hypot():
    if not np:
        skip("NumPy not installed")
    assert abs(lambdify((a, b), hypot(a, b), 'numpy')(3, 4) - 5) <= NUMPY_DEFAULT_EPSILON


def test_hypot():
    x, y = symbols('x y')

    # Expand
    assert hypot(x, y).expand(func=True) - (x**2 + y**2)**S.Half == 0

    # Diff
    assert hypot(17*x, 42*y).diff(x).expand(func=True) - hypot(17*x, 42*y).expand(func=True).diff(x) == 0
    assert hypot(17*x, 42*y).diff(y).expand(func=True) - hypot(17*x, 42*y).expand(func=True).diff(y) == 0

    assert hypot(17*x, 42*y).diff(x).expand(func=True) - 2*17*17*x*((17*x)**2 + (42*y)**2)**Rational(-1, 2)/2 == 0
    assert hypot(17*x, 42*y).diff(y).expand(func=True) - 2*42*42*y*((17*x)**2 + (42*y)**2)**Rational(-1, 2)/2 == 0


def test_hypot():
    assert hypot(0, 0) == 0
    assert hypot(0, 0.33) == mpf(0.33)
    assert hypot(0.33, 0) == mpf(0.33)
    assert hypot(-0.33, 0) == mpf(0.33)
    assert hypot(3, 4) == mpf(5)

