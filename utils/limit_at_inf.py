
def limit_at_inf(num, den, x):
    """
    Find the limit of a rational function
    at oo
    """
    # pwr = degree(num) - degree(den)
    pwr = -val_at_inf(num, den, x)
    # Numerator has a greater degree than denominator
    # Limit at infinity would depend on the sign of the
    # leading coefficients of numerator and denominator
    if pwr > 0:
        return oo*sign(num.LC()/den.LC())
    # Degree of numerator is equal to that of denominator
    # Limit at infinity is just the ratio of leading coeffs
    elif pwr == 0:
        return num.LC()/den.LC()
    # Degree of numerator is less than that of denominator
    # Limit at infinity is just 0
    else:
        return 0

