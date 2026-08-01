
def test_sympy__stats__rv__RandomMatrixSymbol():
    from sympy.stats.rv import RandomMatrixSymbol
    from sympy.stats.random_matrix import RandomMatrixPSpace
    pspace = RandomMatrixPSpace('P')
    assert _test_args(RandomMatrixSymbol('M', 3, 3, pspace))

