
def test_sympy__stats__random_matrix_models__CircularUnitaryEnsembleModel():
    from sympy.stats.random_matrix_models import CircularUnitaryEnsembleModel
    assert _test_args(CircularUnitaryEnsembleModel('U', 3))

