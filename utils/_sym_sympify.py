
def _sym_sympify(arg):
    """
    Converts an arbitrary expression to a type that can be used inside SymPy.
    As generally strings are unwise to use in the expressions,
    it returns the Symbol of argument if the string type argument is passed.

    Parameters
    =========

    arg: The parameter to be converted to be used in SymPy.

    Returns
    =======

    The converted parameter.

    """
    if isinstance(arg, str):
        return Symbol(arg)
    else:
        return _sympify(arg)

