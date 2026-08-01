
def _pow_float(inter, power):
    """Evaluates an interval raised to a floating point."""
    power_rational = nsimplify(power)
    num, denom = power_rational.as_numer_denom()
    if num % 2 == 0:
        start = abs(inter.start)**power
        end = abs(inter.end)**power
        if start < 0:
            ret = interval(0, max(start, end))
        else:
            ret = interval(start, end)
        return ret
    elif denom % 2 == 0:
        if inter.end < 0:
            return interval(-float('inf'), float('inf'), is_valid=False)
        elif inter.start < 0:
            return interval(0, inter.end**power, is_valid=None)
        else:
            return interval(inter.start**power, inter.end**power)
    else:
        if inter.start < 0:
            start = -abs(inter.start)**power
        else:
            start = inter.start**power

        if inter.end < 0:
            end = -abs(inter.end)**power
        else:
            end = inter.end**power

        return interval(start, end, is_valid=inter.is_valid)

