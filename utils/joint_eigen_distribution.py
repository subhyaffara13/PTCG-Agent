
def joint_eigen_distribution(mat):
    """
    For obtaining joint probability distribution
    of eigen values of random matrix.

    Parameters
    ==========

    mat: RandomMatrixSymbol
        The matrix symbol whose eigen values are to be considered.

    Returns
    =======

    Lambda

    Examples
    ========

    >>> from sympy.stats import GaussianUnitaryEnsemble as GUE
    >>> from sympy.stats import joint_eigen_distribution
    >>> U = GUE('U', 2)
    >>> joint_eigen_distribution(U)
    Lambda((l[1], l[2]), exp(-l[1]**2 - l[2]**2)*Product(Abs(l[_i] - l[_j])**2, (_j, _i + 1, 2), (_i, 1, 1))/pi)
    """
    if not isinstance(mat, RandomMatrixSymbol):
        raise ValueError("%s is not of type, RandomMatrixSymbol."%(mat))
    return mat.pspace.model.joint_eigen_distribution()


def JointEigenDistribution(mat):
    """
    Creates joint distribution of eigen values of matrices with random
    expressions.

    Parameters
    ==========

    mat: Matrix
        The matrix under consideration.

    Returns
    =======

    JointDistributionHandmade

    Examples
    ========

    >>> from sympy.stats import Normal, JointEigenDistribution
    >>> from sympy import Matrix
    >>> A = [[Normal('A00', 0, 1), Normal('A01', 0, 1)],
    ... [Normal('A10', 0, 1), Normal('A11', 0, 1)]]
    >>> JointEigenDistribution(Matrix(A))
    JointDistributionHandmade(-sqrt(A00**2 - 2*A00*A11 + 4*A01*A10 + A11**2)/2
    + A00/2 + A11/2, sqrt(A00**2 - 2*A00*A11 + 4*A01*A10 + A11**2)/2 + A00/2 + A11/2)

    """
    eigenvals = mat.eigenvals(multiple=True)
    if not all(is_random(eigenval) for eigenval in set(eigenvals)):
        raise ValueError("Eigen values do not have any random expression, "
                         "joint distribution cannot be generated.")
    return JointDistributionHandmade(*eigenvals)

