
def test_bernoulli_rewrite():
    from sympy.functions.elementary.piecewise import Piecewise
    n = Symbol('n', integer=True, nonnegative=True)

    assert bernoulli(-1).rewrite(zeta) == pi**2/6
    assert bernoulli(-2).rewrite(zeta) == 2*zeta(3)
    assert not bernoulli(n, -3).rewrite(zeta).has(harmonic)
    assert bernoulli(-4, x).rewrite(zeta) == 4*zeta(5, x)
    assert isinstance(bernoulli(n, x).rewrite(zeta), Piecewise)
    assert bernoulli(n+1, x).rewrite(zeta) == -(n+1) * zeta(-n, x)

