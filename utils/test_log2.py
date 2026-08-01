
def test_log2():
    e = log(-1/x)
    assert e.nseries(x, n=5) == -log(x) + log(-1)


def test_log2():
    if not np:
        skip("NumPy not installed")
    assert abs(lambdify((a,), log2(a), 'numpy')(256) - 8) <= NUMPY_DEFAULT_EPSILON


def test_log2():
    # Eval
    assert log2(8) == 3
    assert log2(pi) != log(pi)/log(2)  # log2 should *save* (CPU) instructions

    x = Symbol('x', real=True)
    assert log2(x) != log(x)/log(2)
    assert log2(2**x) == x

    # Expand
    assert log2(x).expand(func=True) - log(x)/log(2) == 0

    # Diff
    assert log2(42*x).diff() - 1/(log(2)*x) == 0
    assert log2(42*x).diff() - log2(42*x).expand(func=True).diff(x) == 0

