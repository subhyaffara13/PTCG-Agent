
def test_sympy__stats__random_matrix_models__CircularOrthogonalEnsembleModel():
    from sympy.stats.random_matrix_models import CircularOrthogonalEnsembleModel
    assert _test_args(CircularOrthogonalEnsembleModel('O', 3))

