
def GaussianUnitaryEnsemble(sym, dim):
    """
    Represents Gaussian Unitary Ensembles.

    Examples
    ========

    >>> from sympy.stats import GaussianUnitaryEnsemble as GUE, density
    >>> from sympy import MatrixSymbol
    >>> G = GUE('U', 2)
    >>> X = MatrixSymbol('X', 2, 2)
    >>> density(G)(X)
    exp(-Trace(X**2))/(2*pi**2)
    """
    sym, dim = _symbol_converter(sym), _sympify(dim)
    model = GaussianUnitaryEnsembleModel(sym, dim)
    rmp = RandomMatrixPSpace(sym, model=model)
    return RandomMatrixSymbol(sym, dim, dim, pspace=rmp)

