
def pretty_print(expr, **kwargs):
    """Prints expr in pretty form.

    pprint is just a shortcut for this function.

    Parameters
    ==========

    expr : expression
        The expression to print.

    wrap_line : bool, optional (default=True)
        Line wrapping enabled/disabled.

    num_columns : int or None, optional (default=None)
        Number of columns before line breaking (default to None which reads
        the terminal width), useful when using SymPy without terminal.

    use_unicode : bool or None, optional (default=None)
        Use unicode characters, such as the Greek letter pi instead of
        the string pi.

    full_prec : bool or string, optional (default="auto")
        Use full precision.

    order : bool or string, optional (default=None)
        Set to 'none' for long expressions if slow; default is None.

    use_unicode_sqrt_char : bool, optional (default=True)
        Use compact single-character square root symbol (when unambiguous).

    root_notation : bool, optional (default=True)
        Set to 'False' for printing exponents of the form 1/n in fractional form.
        By default exponent is printed in root form.

    mat_symbol_style : string, optional (default="plain")
        Set to "bold" for printing MatrixSymbols using a bold mathematical symbol face.
        By default the standard face is used.

    imaginary_unit : string, optional (default="i")
        Letter to use for imaginary unit when use_unicode is True.
        Can be "i" (default) or "j".
    """
    print(pretty(expr, **kwargs))

