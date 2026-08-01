
def recast_to_symbols(eqs, symbols):
    """
    Return (e, s, d) where e and s are versions of *eqs* and
    *symbols* in which any non-Symbol objects in *symbols* have
    been replaced with generic Dummy symbols and d is a dictionary
    that can be used to restore the original expressions.

    Examples
    ========

    >>> from sympy.solvers.solvers import recast_to_symbols
    >>> from sympy import symbols, Function
    >>> x, y = symbols('x y')
    >>> fx = Function('f')(x)
    >>> eqs, syms = [fx + 1, x, y], [fx, y]
    >>> e, s, d = recast_to_symbols(eqs, syms); (e, s, d)
    ([_X0 + 1, x, y], [_X0, y], {_X0: f(x)})

    The original equations and symbols can be restored using d:

    >>> assert [i.xreplace(d) for i in eqs] == eqs
    >>> assert [d.get(i, i) for i in s] == syms

    """
    if not iterable(eqs) and iterable(symbols):
        raise ValueError('Both eqs and symbols must be iterable')
    orig = list(symbols)
    symbols = list(ordered(symbols))
    swap_sym = {}
    i = 0
    for s in symbols:
        if not isinstance(s, Symbol) and s not in swap_sym:
            swap_sym[s] = Dummy('X%d' % i)
            i += 1
    new_f = []
    for i in eqs:
        isubs = getattr(i, 'subs', None)
        if isubs is not None:
            new_f.append(isubs(swap_sym))
        else:
            new_f.append(i)
    restore = {v: k for k, v in swap_sym.items()}
    return new_f, [swap_sym.get(i, i) for i in orig], restore

