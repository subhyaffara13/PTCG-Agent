
def test_sympy__integrals__laplace__LaplaceTransform():
    from sympy.integrals.laplace import LaplaceTransform
    assert _test_args(LaplaceTransform(2, x, y))

