
def random_symbols(expr):
    """
    Returns all RandomSymbols within a SymPy Expression.
    """
    atoms = getattr(expr, 'atoms', None)
    if atoms is not None:
        comp = lambda rv: rv.symbol.name
        l = list(atoms(RandomSymbol))
        return sorted(l, key=comp)
    else:
        return []

