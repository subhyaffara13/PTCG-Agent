
def test_multivariate_laplace():
    raises(ValueError, lambda: Laplace('T', [1, 2], [[1, 2], [2, 1]]))
    L = Laplace('L', [1, 0], [[1, 0], [0, 1]])
    L2 = MultivariateLaplace('L2', [1, 0], [[1, 0], [0, 1]])
    assert density(L)(2, 3) == exp(2)*besselk(0, sqrt(39))/pi
    L1 = Laplace('L1', [1, 2], [[x, 0], [0, y]])
    assert density(L1)(0, 1) == \
        exp(2/y)*besselk(0, sqrt((2 + 4/y + 1/x)/y))/(pi*sqrt(x*y))
    assert L.pspace.distribution.set == ProductSet(S.Reals, S.Reals)
    assert L.pspace.distribution == L2.pspace.distribution

