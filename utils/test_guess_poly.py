
def test_guess_poly():
    # polynomial equations
    assert guess_solve_strategy( S(4), x )  # == GS_POLY
    assert guess_solve_strategy( x, x )  # == GS_POLY
    assert guess_solve_strategy( x + a, x )  # == GS_POLY
    assert guess_solve_strategy( 2*x, x )  # == GS_POLY
    assert guess_solve_strategy( x + sqrt(2), x)  # == GS_POLY
    assert guess_solve_strategy( x + 2**Rational(1, 4), x)  # == GS_POLY
    assert guess_solve_strategy( x**2 + 1, x )  # == GS_POLY
    assert guess_solve_strategy( x**2 - 1, x )  # == GS_POLY
    assert guess_solve_strategy( x*y + y, x )  # == GS_POLY
    assert guess_solve_strategy( x*exp(y) + y, x)  # == GS_POLY
    assert guess_solve_strategy(
        (x - y**3)/(y**2*sqrt(1 - y**2)), x)  # == GS_POLY

