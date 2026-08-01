
def test_sympy__integrals__risch__NonElementaryIntegral():
    from sympy.integrals.risch import NonElementaryIntegral
    assert _test_args(NonElementaryIntegral(exp(-x**2), x))

