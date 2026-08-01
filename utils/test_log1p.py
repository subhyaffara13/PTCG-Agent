
def test_log1p():
    if not np:
        skip("NumPy not installed")

    f = lambdify((a,), log1p(a), 'numpy')
    assert abs(f(1e-99) - 1e-99) <= 1e-99 * NUMPY_DEFAULT_EPSILON


def test_log1p():
    # Eval
    assert log1p(0) == 0
    d = S(10)
    assert expand_log(log1p(d**-1000) - log(d**1000 + 1) + log(d**1000)) == 0

    x = Symbol('x', real=True)

    # Expand and rewrite
    assert log1p(x).expand(func=True) - log(x + 1) == 0
    assert log1p(x).rewrite('tractable') - log(x + 1) == 0
    assert log1p(x).rewrite('log') - log(x + 1) == 0

    # Precision
    assert not abs(log(1e-99 + 1).evalf() - 1e-99) < 1e-100  # for comparison
    assert abs(expand_log(log1p(1e-99)).evalf() - 1e-99) < 1e-100

    # Properties
    assert log1p(-2**Rational(-1, 2)).is_real

    assert not log1p(-1).is_finite
    assert log1p(pi).is_finite

    assert not log1p(x).is_positive
    assert log1p(Symbol('y', positive=True)).is_positive

    assert not log1p(x).is_zero
    assert log1p(Symbol('z', zero=True)).is_zero

    assert not log1p(x).is_nonnegative
    assert log1p(Symbol('o', nonnegative=True)).is_nonnegative

    # Diff
    assert log1p(42*x).diff(x) - 42/(42*x + 1) == 0
    assert log1p(42*x).diff(x) - log1p(42*x).expand(func=True).diff(x) == 0


def test_log1p():
    mp.dps = 15
    assert log1p(0) == 0
    assert log1p(3).ae(log(1+3))
    assert log1p(inf) == inf
    assert log1p(1e-50).ae(1e-50)
    assert (log1p(1e-10)*1e10).ae(0.99999999995)

