
def to_int_repr(clauses, symbols):
    """
    Takes clauses in CNF format and puts them into an integer representation.

    Examples
    ========

    >>> from sympy.logic.boolalg import to_int_repr
    >>> from sympy.abc import x, y
    >>> to_int_repr([x | y, y], [x, y]) == [{1, 2}, {2}]
    True

    """

    # Convert the symbol list into a dict
    symbols = dict(zip(symbols, range(1, len(symbols) + 1)))

    def append_symbol(arg, symbols):
        if isinstance(arg, Not):
            return -symbols[arg.args[0]]
        else:
            return symbols[arg]

    return [{append_symbol(arg, symbols) for arg in Or.make_args(c)}
            for c in clauses]

