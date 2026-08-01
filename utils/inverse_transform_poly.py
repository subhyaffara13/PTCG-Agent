
def inverse_transform_poly(num, den, x):
    """
    A function to make the substitution
    x -> 1/x in a rational function that
    is represented using Poly objects for
    numerator and denominator.
    """
    # Declare for reuse
    one = Poly(1, x)
    xpoly = Poly(x, x)

    # Check if degree of numerator is same as denominator
    pwr = val_at_inf(num, den, x)
    if pwr >= 0:
        # Denominator has greater degree. Substituting x with
        # 1/x would make the extra power go to the numerator
        if num.expr != 0:
            num = num.transform(one, xpoly) * x**pwr
            den = den.transform(one, xpoly)
    else:
        # Numerator has greater degree. Substituting x with
        # 1/x would make the extra power go to the denominator
        num = num.transform(one, xpoly)
        den = den.transform(one, xpoly) * x**(-pwr)
    return num.cancel(den, include=True)

