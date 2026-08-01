
def _extract_decimal_digits_info(decimal: Decimal) -> tuple[int, int]:
    """Compute the total number of digits and decimal places for a given [`Decimal`][decimal.Decimal] instance.

    This function handles both normalized and non-normalized Decimal instances.
    Example: Decimal('1.230') -> 4 digits, 3 decimal places

    Args:
        decimal (Decimal): The decimal number to analyze.

    Returns:
        tuple[int, int]: A tuple containing the number of decimal places and total digits.

    Though this could be divided into two separate functions, the logic is easier to follow if we couple the computation
    of the number of decimals and digits together.
    """
    try:
        decimal_tuple = decimal.as_tuple()

        assert isinstance(decimal_tuple.exponent, int)

        exponent = decimal_tuple.exponent
        num_digits = len(decimal_tuple.digits)

        if exponent >= 0:
            # A positive exponent adds that many trailing zeros
            # Ex: digit_tuple=(1, 2, 3), exponent=2 -> 12300 -> 0 decimal places, 5 digits
            num_digits += exponent
            decimal_places = 0
        else:
            # If the absolute value of the negative exponent is larger than the
            # number of digits, then it's the same as the number of digits,
            # because it'll consume all the digits in digit_tuple and then
            # add abs(exponent) - len(digit_tuple) leading zeros after the decimal point.
            # Ex: digit_tuple=(1, 2, 3), exponent=-2 -> 1.23 -> 2 decimal places, 3 digits
            # Ex: digit_tuple=(1, 2, 3), exponent=-4 -> 0.0123 -> 4 decimal places, 4 digits
            decimal_places = abs(exponent)
            num_digits = max(num_digits, decimal_places)

        return decimal_places, num_digits
    except (AssertionError, AttributeError):
        raise TypeError(f'Unable to extract decimal digits info from supplied value {decimal}')

