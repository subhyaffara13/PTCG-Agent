
def test_rational_laurent_series():
    """
    This function tests the computation of coefficients
    of Laurent series of a rational function.

    Each test case has 5 values -

    1. num - Numerator of the rational function.
    2. den - Denominator of the rational function.
    3. x0 - Point about which Laurent series is to
       be calculated.
    4. mul - Multiplicity of x0 if x0 is a pole of
       the rational function (0 otherwise).
    5. n - Number of terms upto which the series
       is to be calculated.
    """
    tests = [
    # Laurent series about simple pole (Multiplicity = 1)
    (
        Poly(x**2 - 3*x + 9, x, extension=True),
        Poly(x**2 - x, x, extension=True),
        S(1), 1, 6,
        {1: 7, 0: -8, -1: 9, -2: -9, -3: 9, -4: -9}
    ),
    # Laurent series about multiple pole (Multiplicity > 1)
    (
        Poly(64*x**3 - 1728*x + 1216, x, extension=True),
        Poly(64*x**4 - 80*x**3 - 831*x**2 + 1809*x - 972, x, extension=True),
        S(9)/8, 2, 3,
        {0: S(32177152)/46521675, 2: S(1019)/984, -1: S(11947565056)/28610830125, \
        1: S(209149)/75645}
    ),
    (
        Poly(1, x, extension=True),
        Poly(x**5 + (-4*sqrt(2) - 1)*x**4 + (4*sqrt(2) + 12)*x**3 + (-12 - 8*sqrt(2))*x**2 \
        + (4 + 8*sqrt(2))*x - 4, x, extension=True),
        sqrt(2), 4, 6,
        {4: 1 + sqrt(2), 3: -3 - 2*sqrt(2), 2: Mul(-1, -3 - 2*sqrt(2), evaluate=False)/(-1 \
        + sqrt(2)), 1: (-3 - 2*sqrt(2))/(-1 + sqrt(2))**2, 0: Mul(-1, -3 - 2*sqrt(2), evaluate=False \
        )/(-1 + sqrt(2))**3, -1: (-3 - 2*sqrt(2))/(-1 + sqrt(2))**4}
    ),
    # Laurent series about oo
    (
        Poly(x**5 - 4*x**3 + 6*x**2 + 10*x - 13, x, extension=True),
        Poly(x**2 - 5, x, extension=True),
        oo, 3, 6,
        {3: 1, 2: 0, 1: 1, 0: 6, -1: 15, -2: 17}
    ),
    # Laurent series at x0 where x0 is not a pole of the function
    # Using multiplicity as 0 (as x0 will not be a pole)
    (
        Poly(3*x**3 + 6*x**2 - 2*x + 5, x, extension=True),
        Poly(9*x**4 - x**3 - 3*x**2 + 4*x + 4, x, extension=True),
        S(2)/5, 0, 1,
        {0: S(3345)/3304, -1: S(399325)/2729104, -2: S(3926413375)/4508479808, \
        -3: S(-5000852751875)/1862002160704, -4: S(-6683640101653125)/6152055138966016}
    ),
    (
        Poly(-7*x**2 + 2*x - 4, x, extension=True),
        Poly(7*x**5 + 9*x**4 + 8*x**3 + 3*x**2 + 6*x + 9, x, extension=True),
        oo, 0, 6,
        {0: 0, -2: 0, -5: -S(71)/49, -1: 0, -3: -1, -4: S(11)/7}
    )]
    for num, den, x0, mul, n, ser in tests:
        assert ser == rational_laurent_series(num, den, x, x0, mul, n)

