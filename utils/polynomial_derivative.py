
def polynomial_derivative(coefficients):
    """Compute the first derivative of a polynomial.

    Evaluate the derivative of ``x³ - 4 x² - 17 x + 60``:

    >>> coefficients = [1, -4, -17, 60]
    >>> derivative_coefficients = polynomial_derivative(coefficients)
    >>> derivative_coefficients
    [3, -8, -17]

    Note that polynomial coefficients are specified in descending power order.

    Supports all numeric types: int, float, complex, Decimal, Fraction.
    """
    n = len(coefficients)
    powers = reversed(range(1, n))
    return list(map(mul, coefficients, powers))

