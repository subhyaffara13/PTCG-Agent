
def time_to_expr_eqs_165x165():
    eqs = eqs_165x165()
    assert [ R_165.from_expr(eq.as_expr()) for eq in eqs ] == eqs

