
def test_sympy__stats__random_matrix_models__CircularSymplecticEnsembleModel():
    from sympy.stats.random_matrix_models import CircularSymplecticEnsembleModel
    assert _test_args(CircularSymplecticEnsembleModel('S', 3))

