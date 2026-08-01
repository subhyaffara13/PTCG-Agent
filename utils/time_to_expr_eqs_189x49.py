
def time_to_expr_eqs_189x49():
    eqs = eqs_189x49()
    assert [ R_49.from_expr(eq.as_expr()) for eq in eqs ] == eqs

