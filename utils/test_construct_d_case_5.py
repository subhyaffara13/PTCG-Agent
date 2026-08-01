
def test_construct_d_case_5():
    """
    This function tests the Case 5 in the step
    to calculate coefficients of the d-vector.

    Each test case has 3 values -

    1. num - Numerator of the rational function a(x).
    2. den - Denominator of the rational function a(x).
    3. d - The d-vector.
    """
    tests = [
    (
        Poly(2*x**3 + x**2 + x - 2, x, extension=True),
        Poly(9*x**3 + 5*x**2 + 2*x - 1, x, extension=True),
        [[sqrt(2)/3, -sqrt(2)/108], [-sqrt(2)/3, sqrt(2)/108]]
    ),
    (
        Poly(3*x**5 + x**4 - x**3 + x**2 - 2*x - 2, x, domain='ZZ'),
        Poly(9*x**5 + 7*x**4 + 3*x**3 + 2*x**2 + 5*x + 7, x, domain='ZZ'),
        [[sqrt(3)/3, -2*sqrt(3)/27], [-sqrt(3)/3, 2*sqrt(3)/27]]
    ),
    (
        Poly(x**2 - x + 1, x, domain='ZZ'),
        Poly(3*x**2 + 7*x + 3, x, domain='ZZ'),
        [[sqrt(3)/3, -5*sqrt(3)/9], [-sqrt(3)/3, 5*sqrt(3)/9]]
    )]
    for num, den, d in tests:
        # Multiplicity of oo is 0
        ser = rational_laurent_series(num, den, x, oo, 0, 1)
        assert construct_d_case_5(ser) == d

