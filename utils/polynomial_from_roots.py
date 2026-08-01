
def polynomial_from_roots(roots):
    """Compute a polynomial's coefficients from its roots.

    >>> roots = [5, -4, 3]            # (x - 5) * (x + 4) * (x - 3)
    >>> polynomial_from_roots(roots)  # x³ - 4 x² - 17 x + 60
    [1, -4, -17, 60]

    Note that polynomial coefficients are specified in descending power order.

    Supports all numeric types: int, float, complex, Decimal, Fraction.
    """

    # This recipe differs from the one in itertools docs in that it
    # applies list() after each call to convolve().  This avoids
    # hitting stack limits with nested generators.

    poly = [1]
    for root in roots:
        poly = list(convolve(poly, (1, -root)))
    return poly

