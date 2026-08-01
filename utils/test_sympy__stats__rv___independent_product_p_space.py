
def test_sympy__stats__rv__IndependentProductPSpace():
    from sympy.stats.rv import IndependentProductPSpace
    from sympy.stats.crv import SingleContinuousPSpace
    A = SingleContinuousPSpace(x, nd)
    B = SingleContinuousPSpace(y, nd)
    assert _test_args(IndependentProductPSpace(A, B))

