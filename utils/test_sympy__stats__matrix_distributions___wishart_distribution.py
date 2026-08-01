
def test_sympy__stats__matrix_distributions__WishartDistribution():
    from sympy.stats.matrix_distributions import WishartDistribution
    from sympy.matrices.dense import Matrix
    assert _test_args(WishartDistribution(3, Matrix([[1, 0], [0, 1]])))

