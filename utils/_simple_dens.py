
def _simple_dens(f, symbols):
    # when checking if a denominator is zero, we can just check the
    # base of powers with nonzero exponents since if the base is zero
    # the power will be zero, too. To keep it simple and fast, we
    # limit simplification to exponents that are Numbers
    dens = set()
    for d in denoms(f, symbols):
        if d.is_Pow and d.exp.is_Number:
            if d.exp.is_zero:
                continue  # foo**0 is never 0
            d = d.base
        dens.add(d)
    return dens

