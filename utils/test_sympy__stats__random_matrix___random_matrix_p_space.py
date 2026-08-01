
def test_sympy__stats__random_matrix__RandomMatrixPSpace():
    from sympy.stats.random_matrix import RandomMatrixPSpace
    from sympy.stats.random_matrix_models import RandomMatrixEnsembleModel
    model = RandomMatrixEnsembleModel('R', 3)
    assert _test_args(RandomMatrixPSpace('P', model=model))

