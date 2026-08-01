
def test_guess_rational_cv():
    # rational functions
    assert guess_solve_strategy( (x + 1)/(x**2 + 2), x)  # == GS_RATIONAL
    assert guess_solve_strategy(
        (x - y**3)/(y**2*sqrt(1 - y**2)), y)  # == GS_RATIONAL_CV_1

    # rational functions via the change of variable y -> x**n
    assert guess_solve_strategy( (sqrt(x) + 1)/(x**Rational(1, 3) + sqrt(x) + 1), x ) \

