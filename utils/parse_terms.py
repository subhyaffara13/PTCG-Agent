
def parse_terms(expr: sympy.Expr, var: sympy.Symbol) -> list[Term] | None:
    """Parse expression into terms."""
    if not isinstance(expr, sympy.Add):
        # Single term
        term = parse_single_term(expr, var)
        return [term] if term else []

    terms = []
    for arg in expr.args:
        term = parse_single_term(arg, var)
        if term:
            terms.append(term)
        else:
            return None  # If any term fails to parse, fail completely

    return terms

