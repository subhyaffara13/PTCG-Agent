
def test_harmonic_rewrite():
    from sympy.functions.elementary.piecewise import Piecewise
    n = Symbol("n")
    m = Symbol("m", integer=True, positive=True)
    x1 = Symbol("x1", positive=True)
    x2 = Symbol("x2", negative=True)

    assert harmonic(n).rewrite(digamma) == polygamma(0, n + 1) + EulerGamma
    assert harmonic(n).rewrite(trigamma) == polygamma(0, n + 1) + EulerGamma
    assert harmonic(n).rewrite(polygamma) == polygamma(0, n + 1) + EulerGamma

    assert harmonic(n,3).rewrite(polygamma) == polygamma(2, n + 1)/2 - polygamma(2, 1)/2
    assert isinstance(harmonic(n,m).rewrite(polygamma), Piecewise)

    assert expand_func(harmonic(n+4)) == harmonic(n) + 1/(n + 4) + 1/(n + 3) + 1/(n + 2) + 1/(n + 1)
    assert expand_func(harmonic(n-4)) == harmonic(n) - 1/(n - 1) - 1/(n - 2) - 1/(n - 3) - 1/n

    assert harmonic(n, m).rewrite("tractable") == harmonic(n, m).rewrite(polygamma)
    assert harmonic(n, x1).rewrite("tractable") == harmonic(n, x1)
    assert harmonic(n, x1 + 1).rewrite("tractable") == zeta(x1 + 1) - zeta(x1 + 1, n + 1)
    assert harmonic(n, x2).rewrite("tractable") == zeta(x2) - zeta(x2, n + 1)

    _k = Dummy("k")
    assert harmonic(n).rewrite(Sum).dummy_eq(Sum(1/_k, (_k, 1, n)))
    assert harmonic(n, m).rewrite(Sum).dummy_eq(Sum(_k**(-m), (_k, 1, n)))

