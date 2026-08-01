
def test_sympy__stats__random_matrix_models__GaussianEnsembleModel():
    from sympy.stats.random_matrix_models import GaussianEnsembleModel
    assert _test_args(GaussianEnsembleModel('G', 3))

