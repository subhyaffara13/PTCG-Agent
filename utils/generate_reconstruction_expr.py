
def generate_reconstruction_expr(terms: list[Term], var: sympy.Symbol) -> sympy.Expr:
    y = var
    reconstruction = sympy.S.Zero
    remainder = y

    for i, term in enumerate(terms):
        if i < len(terms) - 1:
            component = FloorDiv(remainder, term.coefficient)
            remainder = ModularIndexing(remainder, 1, term.coefficient)
        else:
            # Last term should also divide by its coefficient
            component = FloorDiv(remainder, term.coefficient)

        reconstruction += component * term.reconstruction_multiplier

    return reconstruction

