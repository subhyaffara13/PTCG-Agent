
def _g_sig_digits(value, delta):
    """
    Return the number of significant digits to %g-format *value*, assuming that
    it is known with an error of *delta*.
    """
    # For inf or nan, the precision doesn't matter.
    if not math.isfinite(value):
        return 0
    if delta == 0:
        if value == 0:
            # if both value and delta are 0, np.spacing below returns 5e-324
            # which results in rather silly results
            return 3
        # delta = 0 may occur when trying to format values over a tiny range;
        # in that case, replace it by the distance to the closest float.
        delta = abs(np.spacing(value))
    # If e.g. value = 45.67 and delta = 0.02, then we want to round to 2 digits
    # after the decimal point (floor(log10(0.02)) = -2); 45.67 contributes 2
    # digits before the decimal point (floor(log10(45.67)) + 1 = 2): the total
    # is 4 significant digits.  A value of 0 contributes 1 "digit" before the
    # decimal point.
    return max(
        0,
        (math.floor(math.log10(abs(value))) + 1 if value else 1)
        - math.floor(math.log10(delta)))

