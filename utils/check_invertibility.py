
def check_invertibility(terms: list[Term]) -> bool:
    """Check if the terms represent an invertible transformation."""
    if not terms:
        return False

    # Coefficients must be strictly decreasing
    coeffs = [t.coefficient for t in terms]
    if argsort_sym(V.graph.sizevars.shape_env, coeffs) != list(
        reversed(range(len(coeffs)))
    ):
        return False

    # Check mixed-radix property: each coeff[i] = coeff[i+1] * range[i+1]
    expected_coeff = 1
    for term in reversed(terms):
        if not static_eq(term.coefficient, expected_coeff):
            return False
        if term.range is not None:
            expected_coeff *= term.range

    return True

