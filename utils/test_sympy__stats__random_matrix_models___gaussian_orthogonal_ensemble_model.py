
def test_sympy__stats__random_matrix_models__GaussianOrthogonalEnsembleModel():
    from sympy.stats.random_matrix_models import GaussianOrthogonalEnsembleModel
    assert _test_args(GaussianOrthogonalEnsembleModel('U', 3))

