
def test_sympy__stats__random_matrix_models__CircularEnsembleModel():
    from sympy.stats.random_matrix_models import CircularEnsembleModel
    assert _test_args(CircularEnsembleModel('C', 3))

