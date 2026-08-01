
def literal_symbol(literal):
    """
    The symbol in this literal (without the negation).

    Examples
    ========

    >>> from sympy.abc import A
    >>> from sympy.logic.inference import literal_symbol
    >>> literal_symbol(A)
    A
    >>> literal_symbol(~A)
    A

    """

    if literal is True or literal is False:
        return literal
    elif literal.is_Symbol:
        return literal
    elif literal.is_Not:
        return literal_symbol(literal.args[0])
    else:
        raise ValueError("Argument must be a boolean literal.")

