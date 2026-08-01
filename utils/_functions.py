
def _functions(expr, x):
    """ Find the types of functions in expr, to estimate the complexity. """
    return {e.func for e in expr.atoms(Function) if x in e.free_symbols}

