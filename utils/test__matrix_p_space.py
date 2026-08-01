
def test_MatrixPSpace():
    M = MatrixGammaDistribution(1, 2, [[2, 1], [1, 2]])
    MP = MatrixPSpace('M', M, 2, 2)
    assert MP.distribution == M
    raises(ValueError, lambda: MatrixPSpace('M', M, 1.2, 2))

