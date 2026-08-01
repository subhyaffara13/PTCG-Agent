
def level_spacing_distribution(mat):
    """
    For obtaining distribution of level spacings.

    Parameters
    ==========

    mat: RandomMatrixSymbol
        The random matrix symbol whose eigen values are
        to be considered for finding the level spacings.

    Returns
    =======

    Lambda

    Examples
    ========

    >>> from sympy.stats import GaussianUnitaryEnsemble as GUE
    >>> from sympy.stats import level_spacing_distribution
    >>> U = GUE('U', 2)
    >>> level_spacing_distribution(U)
    Lambda(_s, 32*_s**2*exp(-4*_s**2/pi)/pi**2)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Random_matrix#Distribution_of_level_spacings
    """
    return mat.pspace.model.level_spacing_distribution()

