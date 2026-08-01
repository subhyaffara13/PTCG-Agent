
def test_sympy__integrals__laplace__InverseLaplaceTransform():
    from sympy.integrals.laplace import InverseLaplaceTransform
    assert _test_args(InverseLaplaceTransform(2, x, y, 0))

