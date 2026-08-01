
def test_JointEigenDistribution():
    A = Matrix([[Normal('A00', 0, 1), Normal('A01', 1, 1)],
                [Beta('A10', 1, 1), Beta('A11', 1, 1)]])
    assert JointEigenDistribution(A) == \
    JointDistributionHandmade(-sqrt(A[0, 0]**2 - 2*A[0, 0]*A[1, 1] + 4*A[0, 1]*A[1, 0] + A[1, 1]**2)/2 +
    A[0, 0]/2 + A[1, 1]/2, sqrt(A[0, 0]**2 - 2*A[0, 0]*A[1, 1] + 4*A[0, 1]*A[1, 0] + A[1, 1]**2)/2 + A[0, 0]/2 + A[1, 1]/2)
    raises(ValueError, lambda: JointEigenDistribution(Matrix([[1, 0], [2, 1]])))

