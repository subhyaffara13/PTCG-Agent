
def CircularUnitaryEnsemble(sym, dim):
    """
    Represents Circular Unitary Ensembles.

    Examples
    ========

    >>> from sympy.stats import CircularUnitaryEnsemble as CUE
    >>> from sympy.stats import joint_eigen_distribution
    >>> C = CUE('U', 1)
    >>> joint_eigen_distribution(C)
    Lambda(t[1], Product(Abs(exp(I*t[_j]) - exp(I*t[_k]))**2, (_j, _k + 1, 1), (_k, 1, 0))/(2*pi))

    Note
    ====

    As can be seen above in the example, density of CiruclarUnitaryEnsemble
    is not evaluated because the exact definition is based on haar measure of
    unitary group which is not unique.
    """
    sym, dim = _symbol_converter(sym), _sympify(dim)
    model = CircularUnitaryEnsembleModel(sym, dim)
    rmp = RandomMatrixPSpace(sym, model=model)
    return RandomMatrixSymbol(sym, dim, dim, pspace=rmp)

