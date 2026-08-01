
def test_sympy__stats__random_matrix_models__GaussianUnitaryEnsembleModel():
    from sympy.stats.random_matrix_models import GaussianUnitaryEnsembleModel
    assert _test_args(GaussianUnitaryEnsembleModel('U', 3))

