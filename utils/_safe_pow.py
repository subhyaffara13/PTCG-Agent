import sys

def _safe_pow(base, exponent):
    if exponent < 0:
        raise ValueError("Exponent must be non-negative.")

    if exponent == 0:
        return 1

    half_exp = safe_pow(base, exponent // 2)
    if half_exp is int_oo:
        return int_oo

    # TODO: microoptimization is to avoid overflowing into arbitrary precision
    # and detect overflow prior to doing operations

    result = half_exp * half_exp
    if result > sys.maxsize:
        return int_oo

    if exponent % 2 == 1:
        result *= base
        if result > sys.maxsize:
            return int_oo

    return result

