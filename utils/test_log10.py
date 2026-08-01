
def test_log10():
    if not np:
        skip("NumPy not installed")
    assert abs(lambdify((a,), log10(a), 'numpy')(100) - 2) <= NUMPY_DEFAULT_EPSILON


def test_log10():
    a = log10(interval(1, 2))
    assert a.start == 0
    assert a.end == np.log10(2)
    a = log10(interval(-1, 1))
    assert a.is_valid is None
    a = log10(interval(-3, -1))
    assert a.is_valid is False
    a = log10(-3)
    assert a.is_valid is False
    a = log10(2)
    assert a.start == np.log10(2)
    assert a.end == np.log10(2)


def test_log10():
    x = Symbol('x')

    # Expand
    assert log10(x).expand(func=True) - log(x)/log(10) == 0

    # Diff
    assert log10(42*x).diff(x) - 1/(log(10)*x) == 0
    assert log10(42*x).diff(x) - log10(42*x).expand(func=True).diff(x) == 0

