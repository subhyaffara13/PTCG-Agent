
def test_exp2():
    e = exp(cos(x)).lseries(x)
    assert next(e) == E
    assert next(e) == -E*x**2/2
    assert next(e) == E*x**4/6
    assert next(e) == -31*E*x**6/720


def test_exp2():
    w = Symbol("w")
    e = w**(1 - log(x)/(log(2) + log(x)))
    logw = Symbol("logw")
    assert e.nseries(
        w, 0, 1, logx=logw) == exp(logw*log(2)/(log(x) + log(2)))


def test_exp2():
    e1 = exp(cos(x)).series(x, 0)
    e2 = series(exp(cos(x)), x, 0)
    assert e1 == e2


def test_exp2():
    if not np:
        skip("NumPy not installed")
    assert abs(lambdify((a,), exp2(a), 'numpy')(5) - 32) <= NUMPY_DEFAULT_EPSILON


def test_exp2():
    # Eval
    assert exp2(2) == 4

    x = Symbol('x', real=True)

    # Expand
    assert exp2(x).expand(func=True) - 2**x == 0

    # Diff
    assert exp2(42*x).diff(x) - 42*exp2(42*x)*log(2) == 0
    assert exp2(42*x).diff(x) - exp2(42*x).diff(x) == 0

