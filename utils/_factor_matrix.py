
def _factor_matrix(A, t):
    term = None
    for element in A:
        temp_term = element.as_independent(t)[1]
        if temp_term.has(t):
            term = temp_term
            break

    if term is not None:
        A_factored = (A/term).applyfunc(ratsimp)
        can_factor = _matrix_is_constant(A_factored, t)
        term = (term, A_factored) if can_factor else None

    return term

