
def _is_modular(f, symbol):
    """
    Helper function to check below mentioned types of modular equations.
    ``A - Mod(B, C) = 0``

    A -> This can or cannot be a function of symbol.
    B -> This is surely a function of symbol.
    C -> It is an integer.

    Parameters
    ==========

    f : Expr
        The equation to be checked.

    symbol : Symbol
        The concerned variable for which the equation is to be checked.

    Examples
    ========

    >>> from sympy import symbols, exp, Mod
    >>> from sympy.solvers.solveset import _is_modular as check
    >>> x, y = symbols('x y')
    >>> check(Mod(x, 3) - 1, x)
    True
    >>> check(Mod(x, 3) - 1, y)
    False
    >>> check(Mod(x, 3)**2 - 5, x)
    False
    >>> check(Mod(x, 3)**2 - y, x)
    False
    >>> check(exp(Mod(x, 3)) - 1, x)
    False
    >>> check(Mod(3, y) - 1, y)
    False
    """

    if not f.has(Mod):
        return False

    # extract modterms from f.
    modterms = list(f.atoms(Mod))

    return (len(modterms) == 1 and  # only one Mod should be present
            modterms[0].args[0].has(symbol) and  # B-> function of symbol
            modterms[0].args[1].is_integer and  # C-> to be an integer.
            any(isinstance(term, Mod)
            for term in list(_term_factors(f)))  # free from other funcs
            )

