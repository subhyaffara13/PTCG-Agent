
def test_Sqrt():
    if not np:
        skip("NumPy not installed")
    assert abs(lambdify((a,), Sqrt(a), 'numpy')(4) - 2) <= NUMPY_DEFAULT_EPSILON


def test_Sqrt():
    x = Symbol('x')

    # Expand
    assert Sqrt(x).expand(func=True) - x**S.Half == 0

    # Diff
    assert Sqrt(42*x).diff(x) - 42*(42*x)**(S.Half - 1)/2 == 0
    assert Sqrt(42*x).diff(x) - Sqrt(42*x).expand(func=True).diff(x) == 0

