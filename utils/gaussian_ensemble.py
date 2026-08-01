
def GaussianEnsemble(sym, dim):
    sym, dim = _symbol_converter(sym), _sympify(dim)
    model = GaussianEnsembleModel(sym, dim)
    rmp = RandomMatrixPSpace(sym, model=model)
    return RandomMatrixSymbol(sym, dim, dim, pspace=rmp)

