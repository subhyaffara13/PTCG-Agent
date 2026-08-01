
def test_density_call():
    from sympy.abc import p
    x = Bernoulli('x', p)
    d = density(x)
    assert d(0) == 1 - p
    assert d(S.Zero) == 1 - p
    assert d(5) == 0

    assert 0 in d
    assert 5 not in d
    assert d(S.Zero) == d[S.Zero]

