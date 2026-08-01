
def test_guess_poly_cv():
    # polynomial equations via a change of variable
    assert guess_solve_strategy( sqrt(x) + 1, x )  # == GS_POLY_CV_1
    assert guess_solve_strategy(
        x**Rational(1, 3) + sqrt(x) + 1, x )  # == GS_POLY_CV_1
    assert guess_solve_strategy( 4*x*(1 - sqrt(x)), x )  # == GS_POLY_CV_1

    # polynomial equation multiplying both sides by x**n
    assert guess_solve_strategy( x + 1/x + y, x )  # == GS_POLY_CV_2

