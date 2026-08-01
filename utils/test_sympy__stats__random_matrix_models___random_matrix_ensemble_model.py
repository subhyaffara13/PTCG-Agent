
def test_sympy__stats__random_matrix_models__RandomMatrixEnsembleModel():
    from sympy.stats.random_matrix_models import RandomMatrixEnsembleModel
    assert _test_args(RandomMatrixEnsembleModel('R', 3))

