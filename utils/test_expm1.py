
def test_expm1():
    if not np:
        skip("NumPy not installed")

    f = lambdify((a,), expm1(a), 'numpy')
    assert abs(f(1e-10) - 1e-10 - 5e-21) <= 1e-10 * NUMPY_DEFAULT_EPSILON


def test_expm1():
    # Eval
    assert expm1(0) == 0

    x = Symbol('x', real=True)

    # Expand and rewrite
    assert expm1(x).expand(func=True) - exp(x) == -1
    assert expm1(x).rewrite('tractable') - exp(x) == -1
    assert expm1(x).rewrite('exp') - exp(x) == -1

    # Precision
    assert not ((exp(1e-10).evalf() - 1) - 1e-10 - 5e-21) < 1e-22  # for comparison
    assert abs(expm1(1e-10).evalf() - 1e-10 - 5e-21) < 1e-22

    # Properties
    assert expm1(x).is_real
    assert expm1(x).is_finite

    # Diff
    assert expm1(42*x).diff(x) - 42*exp(42*x) == 0
    assert expm1(42*x).diff(x) - expm1(42*x).expand(func=True).diff(x) == 0


def test_expm1():
    mp.dps = 15
    assert expm1(0) == 0
    assert expm1(3).ae(exp(3)-1)
    assert expm1(inf) == inf
    assert expm1(1e-50).ae(1e-50)
    assert (expm1(1e-10)*1e10).ae(1.00000000005)

