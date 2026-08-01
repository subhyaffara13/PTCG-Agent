
def test_sympy__stats__random_matrix_models__GaussianSymplecticEnsembleModel():
    from sympy.stats.random_matrix_models import GaussianSymplecticEnsembleModel
    assert _test_args(GaussianSymplecticEnsembleModel('U', 3))

