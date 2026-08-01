
def GaussianOrthogonalEnsemble(sym, dim):
    """
    Represents Gaussian Orthogonal Ensembles.

    Examples
    ========

    >>> from sympy.stats import GaussianOrthogonalEnsemble as GOE, density
    >>> from sympy import MatrixSymbol
    >>> G = GOE('U', 2)
    >>> X = MatrixSymbol('X', 2, 2)
    >>> density(G)(X)
    exp(-Trace(X**2)/2)/Integral(exp(-Trace(_H**2)/2), _H)
    """
    sym, dim = _symbol_converter(sym), _sympify(dim)
    model = GaussianOrthogonalEnsembleModel(sym, dim)
    rmp = RandomMatrixPSpace(sym, model=model)
    return RandomMatrixSymbol(sym, dim, dim, pspace=rmp)

