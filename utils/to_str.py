
def to_str(value: str | bytes, encoding: str = "utf-8") -> str:
    return value if isinstance(value, str) else value.decode(encoding)


def to_str(
    x: str | bytes, encoding: str | None = None, errors: str | None = None
) -> str:
    if isinstance(x, str):
        return x
    elif not isinstance(x, bytes):
        raise TypeError(f"not expecting type {type(x).__name__}")
    if encoding or errors:
        return x.decode(encoding or "utf-8", errors=errors or "strict")
    return x.decode()


def to_str(
    x: str | bytes, encoding: str | None = None, errors: str | None = None
) -> str:
    if isinstance(x, str):
        return x
    elif not isinstance(x, bytes):
        raise TypeError(f"not expecting type {type(x).__name__}")
    if encoding or errors:
        return x.decode(encoding or "utf-8", errors=errors or "strict")
    return x.decode()


def to_str(s, dps, strip_zeros=True, min_fixed=None, max_fixed=None,
    show_zero_exponent=False):
    """
    Convert a raw mpf to a decimal floating-point literal with at
    most `dps` decimal digits in the mantissa (not counting extra zeros
    that may be inserted for visual purposes).

    The number will be printed in fixed-point format if the position
    of the leading digit is strictly between min_fixed
    (default = min(-dps/3,-5)) and max_fixed (default = dps).

    To force fixed-point format always, set min_fixed = -inf,
    max_fixed = +inf. To force floating-point format, set
    min_fixed >= max_fixed.

    The literal is formatted so that it can be parsed back to a number
    by to_str, float() or Decimal().
    """

    # Special numbers
    if not s[1]:
        if s == fzero:
            if dps: t = '0.0'
            else:   t = '.0'
            if show_zero_exponent:
                t += 'e+0'
            return t
        if s == finf: return '+inf'
        if s == fninf: return '-inf'
        if s == fnan: return 'nan'
        raise ValueError

    if min_fixed is None: min_fixed = min(-(dps//3), -5)
    if max_fixed is None: max_fixed = dps

    # to_digits_exp rounds to floor.
    # This sometimes kills some instances of "...00001"
    sign, digits, exponent = to_digits_exp(s, dps+3)

    # No digits: show only .0; round exponent to nearest
    if not dps:
        if digits[0] in '56789':
            exponent += 1
        digits = ".0"

    else:
        # Rounding up kills some instances of "...99999"
        if len(digits) > dps and digits[dps] in '56789':
            digits = digits[:dps]
            i = dps - 1
            while i >= 0 and digits[i] == '9':
                i -= 1
            if i >= 0:
                digits = digits[:i] + str(int(digits[i]) + 1) + '0' * (dps - i - 1)
            else:
                digits = '1' + '0' * (dps - 1)
                exponent += 1
        else:
            digits = digits[:dps]

        # Prettify numbers close to unit magnitude
        if min_fixed < exponent < max_fixed:
            if exponent < 0:
                digits = ("0"*int(-exponent)) + digits
                split = 1
            else:
                split = exponent + 1
                if split > dps:
                    digits += "0"*(split-dps)
            exponent = 0
        else:
            split = 1

        digits = (digits[:split] + "." + digits[split:])

        if strip_zeros:
            # Clean up trailing zeros
            digits = digits.rstrip('0')
            if digits[-1] == ".":
                digits += "0"

    if exponent == 0 and dps and not show_zero_exponent: return sign + digits
    if exponent >= 0: return sign + digits + "e+" + str(exponent)
    if exponent < 0: return sign + digits + "e" + str(exponent)

