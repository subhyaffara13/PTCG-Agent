
def test_solve_polynomial_cv_2():
    """
    Test for solving on equations that can be converted to a polynomial equation
    multiplying both sides of the equation by x**m
    """
    assert solve(x + 1/x - 1, x) in \
        [[ S.Half + I*sqrt(3)/2, S.Half - I*sqrt(3)/2],
         [ S.Half - I*sqrt(3)/2, S.Half + I*sqrt(3)/2]]

