
def parse_single_term(term: sympy.Expr, var: sympy.Symbol) -> Term | None:
    """Parse a single term and extract coefficient, range, and reconstruction multiplier."""
    # Extract coefficient and expression parts
    coefficient, expr_parts = term.as_coeff_mul()

    if len(expr_parts) == 0:
        # Pure constant term
        return Term(
            coefficient=coefficient,
            range=1,
            original_expr=1,
            reconstruction_multiplier=0,
        )
    elif len(expr_parts) == 1:
        expr = expr_parts[0]
    else:
        # Multiple non-constant factors, too complex
        return None

    # Now determine the range and reconstruction multiplier
    range_val, reconstruction_multiplier = analyze_expression_properties(expr, var)
    if reconstruction_multiplier is None:
        return None

    return Term(
        coefficient=coefficient,
        range=range_val,
        original_expr=expr,
        reconstruction_multiplier=reconstruction_multiplier,
    )

