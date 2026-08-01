
def decompose(path):
    if isinstance(path, str):
        return unicodedata.normalize('NFD', path)
    try:
        path = path.decode('utf-8')
        path = unicodedata.normalize('NFD', path)
        path = path.encode('utf-8')
    except UnicodeError:
        pass  # Not UTF-8
    return path


def decompose(
    decomposition_table: Mapping[OpOverload, Callable[..., Any]] | None,
) -> Generator[Mapping[OpOverload, Callable[..., Any]], None, None]:
    table = decomposition_table or {}
    token = CURRENT_DECOMPOSITION_TABLE.set(table)
    try:
        yield table
    finally:
        CURRENT_DECOMPOSITION_TABLE.reset(token)


def decompose(expr, separate=False):
    """Decomposes an input polynomial into homogeneous ones of
    smaller or equal degree.

    Explanation
    ===========

    Returns a dictionary with keys as the degree of the smaller
    constituting polynomials. Values are the constituting polynomials.

    Parameters
    ==========

    expr : Expr
        Polynomial(SymPy expression).
    separate : bool
        If True then simply return a list of the constituent monomials
        If not then break up the polynomial into constituent homogeneous
        polynomials.

    Examples
    ========

    >>> from sympy.abc import x, y
    >>> from sympy.integrals.intpoly import decompose
    >>> decompose(x**2 + x*y + x + y + x**3*y**2 + y**5)
    {1: x + y, 2: x**2 + x*y, 5: x**3*y**2 + y**5}
    >>> decompose(x**2 + x*y + x + y + x**3*y**2 + y**5, True)
    {x, x**2, y, y**5, x*y, x**3*y**2}
    """
    poly_dict = {}

    if isinstance(expr, Expr) and not expr.is_number:
        if expr.is_Symbol:
            poly_dict[1] = expr
        elif expr.is_Add:
            symbols = expr.atoms(Symbol)
            degrees = [(sum(degree_list(monom, *symbols)), monom)
                       for monom in expr.args]
            if separate:
                return {monom[1] for monom in degrees}
            else:
                for monom in degrees:
                    degree, term = monom
                    if poly_dict.get(degree):
                        poly_dict[degree] += term
                    else:
                        poly_dict[degree] = term
        elif expr.is_Pow:
            _, degree = expr.args
            poly_dict[degree] = expr
        else:  # Now expr can only be of `Mul` type
            degree = 0
            for term in expr.args:
                term_type = len(term.args)
                if term_type == 0 and term.is_Symbol:
                    degree += 1
                elif term_type == 2:
                    degree += term.args[1]
            poly_dict[degree] = expr
    else:
        poly_dict[0] = expr

    if separate:
        return set(poly_dict.values())
    return poly_dict


def decompose(f, *gens, **args):
    """
    Compute functional decomposition of ``f``.

    Examples
    ========

    >>> from sympy import decompose
    >>> from sympy.abc import x

    >>> decompose(x**4 + 2*x**3 - x - 1)
    [x**2 - x - 1, x**2 + x]

    """
    options.allowed_flags(args, ['polys'])

    try:
        F, opt = poly_from_expr(f, *gens, **args)
    except PolificationFailed as exc:
        raise ComputationFailed('decompose', 1, exc)

    result = F.decompose()

    if not opt.polys:
        return [r.as_expr() for r in result]
    else:
        return result


def decompose(path):
    if isinstance(path, str):
        return unicodedata.normalize('NFD', path)
    try:
        path = path.decode('utf-8')
        path = unicodedata.normalize('NFD', path)
        path = path.encode('utf-8')
    except UnicodeError:
        pass  # Not UTF-8
    return path

