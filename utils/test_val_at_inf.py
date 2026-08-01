
def test_val_at_inf():
    """
    This function tests the valuation of rational
    function at oo.

    Each test case has 3 values -

    1. num - Numerator of rational function.
    2. den - Denominator of rational function.
    3. val_inf - Valuation of rational function at oo
    """
    tests = [
    # degree(denom) > degree(numer)
    (
        Poly(10*x**3 + 8*x**2 - 13*x + 6, x),
        Poly(-13*x**10 - x**9 + 5*x**8 + 7*x**7 + 10*x**6 + 6*x**5 - 7*x**4 + 11*x**3 - 8*x**2 + 5*x + 13, x),
         7
    ),
    (
        Poly(1, x),
        Poly(-9*x**4 + 3*x**3 + 15*x**2 - 6*x - 14, x),
         4
    ),
    # degree(denom) == degree(numer)
    (
        Poly(-6*x**3 - 8*x**2 + 8*x - 6, x),
        Poly(-5*x**3 + 12*x**2 - 6*x - 9, x),
         0
    ),
    # degree(denom) < degree(numer)
    (
        Poly(12*x**8 - 12*x**7 - 11*x**6 + 8*x**5 + 3*x**4 - x**3 + x**2 - 11*x, x),
        Poly(-14*x**2 + x, x),
         -6
    ),
    (
        Poly(5*x**6 + 9*x**5 - 11*x**4 - 9*x**3 + x**2 - 4*x + 4, x),
        Poly(15*x**4 + 3*x**3 - 8*x**2 + 15*x + 12, x),
         -2
    )]
    for num, den, val in tests:
        assert val_at_inf(num, den, x) == val

