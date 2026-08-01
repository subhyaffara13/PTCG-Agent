
def parse_latex(sympy, strict=False):
    antlr4 = import_module('antlr4')

    if None in [antlr4, MathErrorListener] or \
            not version('antlr4-python3-runtime').startswith('4.11'):
        raise ImportError("LaTeX parsing requires the antlr4 Python package,"
                          " provided by pip (antlr4-python3-runtime) or"
                          " conda (antlr-python-runtime), version 4.11")

    sympy = sympy.strip()
    matherror = MathErrorListener(sympy)

    stream = antlr4.InputStream(sympy)
    lex = LaTeXLexer(stream)
    lex.removeErrorListeners()
    lex.addErrorListener(matherror)

    tokens = antlr4.CommonTokenStream(lex)
    parser = LaTeXParser(tokens)

    # remove default console error listener
    parser.removeErrorListeners()
    parser.addErrorListener(matherror)

    relation = parser.math().relation()
    if strict and (relation.start.start != 0 or relation.stop.stop != len(sympy) - 1):
        raise LaTeXParsingError("Invalid LaTeX")
    expr = convert_relation(relation)

    return expr


def parse_latex(s, strict=False, backend="antlr"):
    r"""Converts the input LaTeX string ``s`` to a SymPy ``Expr``.

    Parameters
    ==========

    s : str
        The LaTeX string to parse. In Python source containing LaTeX,
        *raw strings* (denoted with ``r"``, like this one) are preferred,
        as LaTeX makes liberal use of the ``\`` character, which would
        trigger escaping in normal Python strings.
    backend : str, optional
        Currently, there are two backends supported: ANTLR, and Lark.
        The default setting is to use the ANTLR backend, which can be
        changed to Lark if preferred.

        Use ``backend="antlr"`` for the ANTLR-based parser, and
        ``backend="lark"`` for the Lark-based parser.

        The ``backend`` option is case-sensitive, and must be in
        all lowercase.
    strict : bool, optional
        This option is only available with the ANTLR backend.

        If True, raise an exception if the string cannot be parsed as
        valid LaTeX. If False, try to recover gracefully from common
        mistakes.

    Examples
    ========

    >>> from sympy.parsing.latex import parse_latex
    >>> expr = parse_latex(r"\frac {1 + \sqrt {\a}} {\b}")
    >>> expr
    (sqrt(a) + 1)/b
    >>> expr.evalf(4, subs=dict(a=5, b=2))
    1.618
    >>> func = parse_latex(r"\int_1^\alpha \dfrac{\mathrm{d}t}{t}", backend="lark")
    >>> func.evalf(subs={"alpha": 2})
    0.693147180559945
    """

    check_matrix_delimiters(s)

    if backend == "antlr":
        _latex = import_module(
            'sympy.parsing.latex._parse_latex_antlr',
            import_kwargs={'fromlist': ['X']})

        if _latex is not None:
            return _latex.parse_latex(s, strict)
    elif backend == "lark":
        return parse_latex_lark(s)
    else:
        raise NotImplementedError(f"Using the '{backend}' backend in the LaTeX" \
                                   " parser is not supported.")

