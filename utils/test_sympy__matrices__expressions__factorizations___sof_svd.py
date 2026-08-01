
def test_sympy__matrices__expressions__factorizations__SofSVD():
    from sympy.matrices.expressions.factorizations import SofSVD
    assert _test_args(SofSVD(X))

